{{/*
Expand the name of the chart.
*/}}
{{- define "learnflow-backend.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "learnflow-backend.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "learnflow-backend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "learnflow-backend.labels" -}}
helm.sh/chart: {{ include "learnflow-backend.chart" . }}
{{ include "learnflow-backend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "learnflow-backend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "learnflow-backend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "learnflow-backend.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "learnflow-backend.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Common environment variables for all services
*/}}
{{- define "learnflow-backend.commonEnv" -}}
- name: ENVIRONMENT
  value: {{ .Values.common.environment | default "production" | quote }}
- name: LOG_LEVEL
  value: {{ .Values.common.logLevel | default "INFO" | quote }}
- name: LOG_FORMAT
  value: {{ .Values.common.logFormat | default "json" | quote }}
- name: DAPR_HTTP_PORT
  value: {{ .Values.dapr.httpPort | default 3500 | quote }}
- name: DAPR_GRPC_PORT
  value: {{ .Values.dapr.grpcPort | default 50001 | quote }}
- name: DAPR_PUBSUB_NAME
  value: {{ .Values.dapr.pubsubName | default "pubsub-kafka" | quote }}
- name: DAPR_STATESTORE_NAME
  value: {{ .Values.dapr.statestoreName | default "statestore-postgres" | quote }}
- name: OPENAI_API_KEY
  valueFrom:
    secretKeyRef:
      name: {{ include "learnflow-backend.fullname" . }}-secrets
      key: openai-api-key
- name: OPENAI_MODEL
  value: {{ .Values.openai.model | default "gpt-4-turbo-preview" | quote }}
- name: OPENAI_TIMEOUT
  value: {{ .Values.openai.timeout | default 30 | quote }}
{{- end }}

{{/*
Dapr annotations for sidecar injection
*/}}
{{- define "learnflow-backend.daprAnnotations" -}}
dapr.io/enabled: "true"
dapr.io/app-id: {{ .appId | quote }}
dapr.io/app-port: {{ .appPort | quote }}
dapr.io/enable-api-logging: "true"
dapr.io/log-level: "info"
{{- end }}
