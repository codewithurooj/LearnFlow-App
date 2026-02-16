# Data Model: LearnFlow Frontend

**Date**: 2026-02-14
**Feature**: learnflow-frontend

## Overview

The frontend is a thin client — it does **not** own a database. All persistent data lives in the backend (PostgreSQL via microservices). The frontend manages ephemeral client-side state and maps backend API responses to TypeScript types.

## Client-Side Entities (TypeScript Types)

### User

```typescript
interface User {
  id: string;          // UUID from Better Auth
  email: string;
  name: string;
  role: "student" | "teacher";
  createdAt: string;   // ISO 8601
}
```

**Source**: Better Auth session
**Storage**: Session cookie (managed by Better Auth)

### ChatMessage

```typescript
interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;           // Markdown content
  codeExamples?: CodeExample[];
  relatedTopics?: string[];
  timestamp: string;
}

interface CodeExample {
  title: string;
  code: string;
  explanation: string;
}
```

**Source**: Triage service response (`/api/v1/triage/route`)
**Storage**: Zustand `chatStore` (in-memory, per session)

### CodeExecution

```typescript
interface CodeExecutionRequest {
  studentId: string;
  code: string;
  exerciseId?: string;
}

interface CodeExecutionResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  executionTimeMs: number;
  memoryUsedMb: number;
  timedOut: boolean;
  errorType?: string;
}
```

**Source**: Code Runner service (`/api/v1/code/execute`)
**Storage**: Zustand `editorStore` (in-memory); code persisted to localStorage (FR-013)

### Exercise

```typescript
interface Exercise {
  exerciseId: string;
  title: string;
  description: string;
  starterCode?: string;
  expectedOutputHint?: string;
}

interface ExerciseSubmission {
  studentId: string;
  exerciseId: string;
  code: string;
}

interface ExerciseResult {
  passed: boolean;
  score: number;           // 0-1
  testResults: TestResult[];
  feedback: string;
  timeSpentSeconds: number;
}

interface TestResult {
  name: string;
  passed: boolean;
  message?: string;
}
```

**Source**: Exercise service (`/api/v1/exercises/generate`, `/api/v1/exercises/submit`)
**Storage**: Zustand `exerciseStore` (in-memory)

### Progress

```typescript
interface ProgressSummary {
  studentId: string;
  overallMastery: number;    // 0-100%
  overallLevel: MasteryLevel;
  topics: TopicMastery[];
  currentStreak: number;
  lastActivity: string;
  totalExercises: number;
  totalQuizzes: number;
}

interface TopicMastery {
  topicId: string;
  topicName: string;
  masteryScore: number;     // 0-100%
  masteryLevel: MasteryLevel;
  levelColor: string;       // hex color
}

interface TopicDetail extends TopicMastery {
  breakdown: {
    exercises: number;
    quizzes: number;
    codeQuality: number;
    streak: number;
  };
  improvementSuggestions: string[];
  lastActivity: string;
}

type MasteryLevel = "Beginner" | "Learning" | "Proficient" | "Mastered";
```

**Source**: Progress service (`/api/v1/progress/{studentId}`)
**Storage**: Zustand `progressStore` (in-memory)

### CodeReview

```typescript
interface CodeReviewResult {
  rating: number;            // 1-5 stars
  correctness: CriterionScore;
  style: CriterionScore;
  efficiency: CriterionScore;
  readability: CriterionScore;
  strengths: string[];
  suggestions: string[];
  encouragement: string;
}

interface CriterionScore {
  score: number;             // 1-5
  feedback: string;
}
```

**Source**: Code Review service (`/api/v1/review/analyze`)
**Storage**: Zustand `editorStore` (in-memory)

### DebugHelp

```typescript
interface DebugResult {
  errorType: string;
  errorLine?: number;
  rootCause: string;
  hint: string;
  solution?: string;
  struggleDetected: boolean;
}
```

**Source**: Debug service (`/api/v1/debug/analyze`, `/api/v1/debug/solution`)
**Storage**: Zustand `editorStore` (in-memory)

### TeacherDashboard (Teacher-only)

```typescript
interface ClassOverview {
  totalStudents: number;
  activeStudents: number;
  averageMastery: number;
  topicDistribution: Record<MasteryLevel, number>;
  recentStruggles: StruggleAlert[];
}

interface StruggleAlert {
  studentId: string;
  studentName: string;
  struggleType: string;
  confidence: number;
  timestamp: string;
  details?: string;
}
```

**Source**: MCP Context server (`/api/v1/context/class/overview`, `/api/v1/context/student/{id}/struggles`)
**Storage**: Zustand (in-memory, polled every 30s)

## State Relationships

```
User (auth session)
 ├── ChatMessage[] (per session, via chatStore)
 ├── CodeExecution (current editor state, via editorStore)
 │    ├── CodeReviewResult (latest review)
 │    └── DebugResult (latest debug help)
 ├── Exercise + ExerciseResult (current exercise, via exerciseStore)
 └── ProgressSummary + TopicDetail[] (mastery data, via progressStore)

Teacher extends User (role="teacher")
 └── ClassOverview + StruggleAlert[] (polled, via teacherStore)
```

## Local Storage Keys

| Key | Purpose | Data |
|-----|---------|------|
| `learnflow:code` | Persist editor code across refreshes (FR-013) | `string` (raw code) |
| `learnflow:language` | Remember last language setting | `string` (always "python" for MVP) |
