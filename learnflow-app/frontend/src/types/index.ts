export type MasteryLevel = "Beginner" | "Learning" | "Proficient" | "Mastered";

export interface User {
  id: string;
  email: string;
  name: string;
  role: "student" | "teacher";
  createdAt: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  codeExamples?: CodeExample[];
  relatedTopics?: string[];
  timestamp: string;
}

export interface CodeExample {
  title: string;
  code: string;
  explanation: string;
}

export interface TriageRequest {
  student_id: string;
  question: string;
  session_id?: string;
  mastery_level?: string;
}

export interface TriageResponse {
  routed_to: string;
  confidence: number;
  response: string;
  sources: string[];
  processing_time_ms: number;
}

export interface CodeExecutionRequest {
  student_id: string;
  code: string;
  exercise_id?: string;
}

export interface CodeExecutionResult {
  stdout: string;
  stderr: string;
  exit_code: number;
  execution_time_ms: number;
  memory_used_mb: number;
  timed_out: boolean;
  error_type?: string;
}

export interface Exercise {
  exercise_id: string;
  title: string;
  description: string;
  starter_code?: string;
  expected_output_hint?: string;
}

export interface ExerciseSubmission {
  student_id: string;
  exercise_id: string;
  code: string;
}

export interface TestResult {
  name: string;
  passed: boolean;
  message?: string;
}

export interface ExerciseResult {
  passed: boolean;
  score: number;
  test_results: TestResult[];
  feedback: string;
  time_spent_seconds: number;
}

export interface ProgressSummary {
  student_id: string;
  overall_mastery: number;
  overall_level: MasteryLevel;
  topics: TopicMastery[];
  current_streak: number;
  last_activity: string;
  total_exercises: number;
  total_quizzes: number;
}

export interface TopicMastery {
  topic_id: string;
  topic_name: string;
  mastery_score: number;
  mastery_level: MasteryLevel;
  level_color: string;
}

export interface TopicDetail extends TopicMastery {
  breakdown: {
    exercises: number;
    quizzes: number;
    code_quality: number;
    streak: number;
  };
  improvement_suggestions: string[];
  last_activity: string;
}

export interface CriterionScore {
  score: number;
  feedback: string;
}

export interface CodeReviewResult {
  rating: number;
  correctness: CriterionScore;
  style: CriterionScore;
  efficiency: CriterionScore;
  readability: CriterionScore;
  strengths: string[];
  suggestions: string[];
  encouragement: string;
}

export interface DebugResult {
  error_type: string;
  error_line?: number;
  root_cause: string;
  hint: string;
  solution?: string;
  struggle_detected: boolean;
}

export interface ClassOverview {
  total_students: number;
  active_students: number;
  average_mastery: number;
  topic_distribution: Record<MasteryLevel, number>;
  recent_struggles: StruggleAlert[];
}

export interface StruggleAlert {
  student_id: string;
  student_name: string;
  struggle_type: string;
  confidence: number;
  timestamp: string;
  details?: string;
}

export interface ReviewRequest {
  student_id: string;
  code: string;
  context?: string;
}

export interface DebugRequest {
  student_id: string;
  code: string;
  error_output: string;
  traceback?: string;
}
