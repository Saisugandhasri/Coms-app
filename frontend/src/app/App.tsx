import { useState } from 'react';
import exampleImage from 'figma:asset/6142dec3cea4fa0b8961ca622ffb036d2bf3be3c.png';
import { AudioPlayer } from './components/AudioPlayer';
import { AnswerInput } from './components/AnswerInput';
import { FeedbackCard } from './components/FeedbackCard';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from './components/ui/button';

interface Exercise {
  id: number;
  audioText: string;
  correctAnswer: string;
  wrongTense: string;
  correctTense: string;
}

interface AnswerState {
  userAnswer: string | null;
  isCorrect: boolean | null;
  submitted: boolean;
}

const exercises: Exercise[] = [
  {
    id: 1,
    audioText: 'I go to the store yesterday',
    correctAnswer: 'I went to the store yesterday',
    wrongTense: 'present tense (go)',
    correctTense: 'past tense (went)',
  },
  {
    id: 2,
    audioText: 'She will meets her friend tomorrow',
    correctAnswer: 'She will meet her friend tomorrow',
    wrongTense: 'present tense with future (will meets)',
    correctTense: 'base form with future (will meet)',
  },
  {
    id: 3,
    audioText: 'They was playing soccer last week',
    correctAnswer: 'They were playing soccer last week',
    wrongTense: 'singular past (was)',
    correctTense: 'plural past (were)',
  },
  {
    id: 4,
    audioText: 'He have finished his homework already',
    correctAnswer: 'He has finished his homework already',
    wrongTense: 'plural present perfect (have)',
    correctTense: 'singular present perfect (has)',
  },
  {
    id: 5,
    audioText: 'We are going to the park last Sunday',
    correctAnswer: 'We went to the park last Sunday',
    wrongTense: 'present continuous (are going)',
    correctTense: 'simple past (went)',
  },
];

export default function App() {
  const [currentExercise, setCurrentExercise] = useState(0);
  const [answers, setAnswers] = useState<AnswerState[]>(
    exercises.map(() => ({ userAnswer: null, isCorrect: null, submitted: false }))
  );

  const exercise = exercises[currentExercise];
  const currentAnswer = answers[currentExercise];

const handleSubmitAnswer = async (answer: string, isAudio: boolean) => {
  try {
    const res = await fetch(
      "http://localhost:8000/api/exercise/tense/answer/text",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          exercise_id: String(exercise.id),
          user_answer: answer,
        }),
      }
    );

    if (!res.ok) {
      throw new Error("Failed to submit answer");
    }

    const data = await res.json();

    const newAnswers = [...answers];
    newAnswers[currentExercise] = {
      userAnswer: data.user_answer,
      isCorrect: data.is_correct,
      submitted: true,
    };

    setAnswers(newAnswers);
  } catch (err) {
    console.error(err);
    alert("Error submitting answer");
  }
};


  const handleNext = () => {
    if (currentExercise < exercises.length - 1) {
      setCurrentExercise(currentExercise + 1);
    }
  };

  const handlePrevious = () => {
    if (currentExercise > 0) {
      setCurrentExercise(currentExercise - 1);
    }
  };

  const getExplanation = () => {
    if (currentAnswer.isCorrect) {
      return `Perfect! You correctly identified that "${exercise.wrongTense}" should be changed to "${exercise.correctTense}" when referring to past actions.`;
    } else {
      return `The sentence uses ${exercise.wrongTense}, but the time indicator requires ${exercise.correctTense}. Remember to match the verb tense with the time context of the sentence.`;
    }
  };

  // Calculate completion stats
  const answeredCount = answers.filter(a => a.submitted).length;
  const correctCount = answers.filter(a => a.isCorrect === true).length;

  return (
    <div className="h-screen bg-gray-50 flex flex-col overflow-hidden">
      {/* Main Content */}
      <main className="flex-1 overflow-hidden flex flex-col">
        <div className="max-w-4xl mx-auto px-6 py-6 w-full flex flex-col h-full">
          {/* Title */}
          <div className="mb-6 flex-shrink-0">
            <h1 className="text-3xl mb-4">Convert the Tense</h1>
          </div>

          {/* Progress */}
          <div className="mb-6 flex-shrink-0">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Exercise {currentExercise + 1} of {exercises.length}</span>
              <span>{answeredCount} answered • {correctCount} correct</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentExercise + 1) / exercises.length) * 100}%` }}
              />
            </div>
          </div>

          <div className="flex-1 flex flex-col min-h-0">
            {/* Audio Player */}
            <div className="mb-4 flex-shrink-0">
              <AudioPlayer audioText={exercise.audioText} />
            </div>

            {/* Answer Input or Feedback */}
            <div className="flex-1 min-h-0 overflow-auto">
              {!currentAnswer.submitted ? (
                <AnswerInput 
                  onSubmit={handleSubmitAnswer}
                  disabled={currentAnswer.submitted}
                />
              ) : currentAnswer.userAnswer && currentAnswer.isCorrect !== null ? (
                <FeedbackCard
                  isCorrect={currentAnswer.isCorrect}
                  userAnswer={currentAnswer.userAnswer}
                  correctAnswer={exercise.correctAnswer}
                  explanation={getExplanation()}
                  onNext={handleNext}
                  isLastQuestion={currentExercise === exercises.length - 1}
                />
              ) : null}
            </div>
          </div>

          {/* Navigation Buttons */}
          <div className="mt-4 flex justify-between flex-shrink-0">
            <Button
              onClick={handlePrevious}
              disabled={currentExercise === 0}
              variant="outline"
              size="lg"
            >
              <ChevronLeft className="w-5 h-5 mr-2" />
              Previous
            </Button>
            <Button
              onClick={handleNext}
              disabled={currentExercise === exercises.length - 1}
              variant="outline"
              size="lg"
            >
              Next
              <ChevronRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}