import { CheckCircle2, XCircle, Lightbulb } from 'lucide-react';
import { Button } from './ui/button';

interface FeedbackCardProps {
  isCorrect: boolean;
  userAnswer: string;
  correctAnswer: string;
  explanation: string;
  onNext: () => void;
  isLastQuestion?: boolean;
}

export function FeedbackCard({ isCorrect, userAnswer, correctAnswer, explanation, onNext, isLastQuestion }: FeedbackCardProps) {
  return (
    <div className={`rounded-lg p-6 shadow-sm border-2 ${
      isCorrect ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
    }`}>
      <div className="flex items-start gap-3 mb-4">
        {isCorrect ? (
          <CheckCircle2 className="w-8 h-8 text-green-600 flex-shrink-0" />
        ) : (
          <XCircle className="w-8 h-8 text-red-600 flex-shrink-0" />
        )}
        <div>
          <h3 className={isCorrect ? 'text-green-800' : 'text-red-800'}>
            {isCorrect ? 'Correct!' : 'Not Quite Right'}
          </h3>
          <p className={`text-sm ${isCorrect ? 'text-green-700' : 'text-red-700'}`}>
            {isCorrect ? 'Great job! Your answer is correct.' : 'Let\'s review your answer.'}
          </p>
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <p className="text-sm text-gray-600 mb-1">Your Answer:</p>
          <p className={`p-3 rounded-md ${
            isCorrect ? 'bg-green-100 text-green-900' : 'bg-red-100 text-red-900'
          }`}>
            "{userAnswer}"
          </p>
        </div>

        {!isCorrect && (
          <div>
            <p className="text-sm text-gray-600 mb-1">Correct Answer:</p>
            <p className="bg-green-100 text-green-900 p-3 rounded-md">
              "{correctAnswer}"
            </p>
          </div>
        )}

        <div className="bg-white border border-gray-200 rounded-md p-4">
          <div className="flex items-start gap-2">
            <Lightbulb className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm mb-1">Explanation:</p>
              <p className="text-sm text-gray-700">{explanation}</p>
            </div>
          </div>
        </div>

        <Button
          onClick={onNext}
          className="w-full bg-blue-600 hover:bg-blue-700"
          size="lg"
        >
          {isLastQuestion ? 'Finish' : 'Next Exercise'}
        </Button>
      </div>
    </div>
  );
}