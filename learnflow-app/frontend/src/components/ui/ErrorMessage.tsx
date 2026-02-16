import { Button } from "./Button";

interface ErrorMessageProps { message: string; onRetry?: () => void; }

export function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
      <p className="text-sm text-red-700">{message}</p>
      {onRetry && <Button variant="outline" size="sm" onClick={onRetry} className="mt-2">Try Again</Button>}
    </div>
  );
}
