#!/bin/bash
#
# LearnFlow Backend Health Check Script
#
# Verifies all backend microservices are running and healthy.
# Usage: ./backend-health.sh [namespace]
#

set -euo pipefail

NAMESPACE="${1:-learnflow}"
TIMEOUT=10

# Service definitions (name:port)
SERVICES=(
    "triage-service:8001"
    "concepts-service:8002"
    "code-runner-service:8003"
    "debug-service:8004"
    "exercise-service:8005"
    "progress-service:8006"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================"
echo "LearnFlow Backend Health Check"
echo "Namespace: $NAMESPACE"
echo "================================================"
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl is not installed${NC}"
    exit 1
fi

# Check namespace exists
if ! kubectl get namespace "$NAMESPACE" &> /dev/null; then
    echo -e "${RED}Error: Namespace '$NAMESPACE' does not exist${NC}"
    exit 1
fi

echo "Checking pod status..."
echo ""

# Get pod status
kubectl get pods -n "$NAMESPACE" -o wide

echo ""
echo "================================================"
echo "Individual Service Health Checks"
echo "================================================"
echo ""

TOTAL=0
HEALTHY=0
UNHEALTHY=0

for service_def in "${SERVICES[@]}"; do
    SERVICE_NAME="${service_def%%:*}"
    SERVICE_PORT="${service_def##*:}"
    TOTAL=$((TOTAL + 1))

    echo -n "Checking $SERVICE_NAME... "

    # Check if pod exists and is running
    POD_STATUS=$(kubectl get pods -n "$NAMESPACE" -l "app=$SERVICE_NAME" -o jsonpath='{.items[0].status.phase}' 2>/dev/null || echo "NotFound")

    if [[ "$POD_STATUS" != "Running" ]]; then
        echo -e "${RED}FAILED${NC} (Pod status: $POD_STATUS)"
        UNHEALTHY=$((UNHEALTHY + 1))
        continue
    fi

    # Port forward and check health endpoint
    POD_NAME=$(kubectl get pods -n "$NAMESPACE" -l "app=$SERVICE_NAME" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

    if [[ -z "$POD_NAME" ]]; then
        echo -e "${RED}FAILED${NC} (No pod found)"
        UNHEALTHY=$((UNHEALTHY + 1))
        continue
    fi

    # Try to check health via kubectl exec
    HEALTH_STATUS=$(kubectl exec -n "$NAMESPACE" "$POD_NAME" -- curl -s -o /dev/null -w "%{http_code}" "http://localhost:$SERVICE_PORT/api/v1/health" 2>/dev/null || echo "000")

    if [[ "$HEALTH_STATUS" == "200" ]]; then
        echo -e "${GREEN}HEALTHY${NC}"
        HEALTHY=$((HEALTHY + 1))
    else
        echo -e "${YELLOW}DEGRADED${NC} (HTTP $HEALTH_STATUS)"
        UNHEALTHY=$((UNHEALTHY + 1))
    fi
done

echo ""
echo "================================================"
echo "Summary"
echo "================================================"
echo ""
echo "Total Services: $TOTAL"
echo -e "Healthy: ${GREEN}$HEALTHY${NC}"
echo -e "Unhealthy: ${RED}$UNHEALTHY${NC}"
echo ""

if [[ $UNHEALTHY -eq 0 ]]; then
    echo -e "${GREEN}All services are healthy!${NC}"
    exit 0
else
    echo -e "${YELLOW}Some services are unhealthy. Check logs:${NC}"
    echo ""
    for service_def in "${SERVICES[@]}"; do
        SERVICE_NAME="${service_def%%:*}"
        echo "  kubectl logs -n $NAMESPACE -l app=$SERVICE_NAME --tail=50"
    done
    exit 1
fi
