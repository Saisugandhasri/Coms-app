import { useState, useEffect } from "react";
import { AudioPlayer } from "./components/AudioPlayer";
import { AnswerInput } from "./components/AnswerInput";
import { FeedbackCard } from "./components/FeedbackCard";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "./components/ui/button";

/* -----------------------------
   Types
------------------------------ */

interface Exercise {
  exercise_id: string;
  sentence: string;
  topic: string;
}

interface AnswerState {
  userAnswer: string | null;
  isCorrect: boolean | null;
  submitted: boolean;
  feedback?: string;
  corrected_sentence?: string;
}

/* -----------------------------
   App
------------------------------ */

export default function App() {
  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [answer, setAnswer] = useState<AnswerState>({
    userAnswer: null,
    isCorrect: null,
    submitted: false,
  });

  const [loading, setLoading] = useState(false);

  // UI counters
  const [currentIndex, setCurrentIndex] = useState(1);
  const [answeredCount, setAnsweredCount] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);

  const TOTAL_EXERCISES = 5;

  /* -----------------------------
     Fetch Exercise
  ------------------------------ */
  const fetchExercise = async () => {
    try {
      setLoading(true);
      const res = await fetch("http://localhost:8000/api/exercise/tense");
      if (!res.ok) throw new Error("Failed to fetch exercise");
      const data = await res.json();

      setExercise(data);
      setAnswer({
        userAnswer: null,
        isCorrect: null,
        submitted: false,
      });
    } catch (err) {
      console.error(err);
      alert("Failed to load exercise");
    } finally {
      setLoading(false);
    }
  };

  /* 🔥 FIX: fetch exercise when index changes */
  useEffect(() => {
    fetchExercise();
  }, [currentIndex]);

  /* -----------------------------
     Submit Answer
  ------------------------------ */
  const handleSubmitAnswer = async (userAnswer: string, isAudio: boolean) => {
    if (!exercise) return;

    try {
      setLoading(true);

      const res = await fetch(
        "http://localhost:8000/api/exercise/tense/answer/text",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            exercise_id: exercise.exercise_id,
            sentence: exercise.sentence,
            user_answer: userAnswer,
          }),
        }
      );

      if (!res.ok) throw new Error("Failed to submit answer");

      const data = await res.json();

      setAnswer({
        userAnswer,
        isCorrect: data.is_correct,
        submitted: true,
        feedback: data.feedback,
        corrected_sentence: data.corrected_sentence,
      });

      setAnsweredCount((prev) => prev + 1);
      if (data.is_correct) {
        setCorrectCount((prev) => prev + 1);
      }
    } catch (err) {
      console.error(err);
      alert("Error submitting answer");
    } finally {
      setLoading(false);
    }
  };

  /* -----------------------------
     Navigation
  ------------------------------ */
  const handleNext = () => {
    if (currentIndex < TOTAL_EXERCISES) {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 1) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  /* -----------------------------
     UI
  ------------------------------ */
  return (
    <div className="h-screen bg-gray-50 flex flex-col overflow-hidden">
      <main className="flex-1 overflow-hidden flex flex-col">
        <div className="max-w-4xl mx-auto px-6 py-6 w-full flex flex-col h-full">

          {/* Title */}
          <div className="mb-6 flex-shrink-0">
            <h1 className="text-3xl mb-4">Convert the Tense</h1>
          </div>

          {/* Progress */}
          <div className="mb-6 flex-shrink-0">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>
                Exercise {currentIndex} of {TOTAL_EXERCISES}
              </span>
              <span>
                {answeredCount} answered • {correctCount} correct
              </span>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{
                  width: `${(currentIndex / TOTAL_EXERCISES) * 100}%`,
                }}
              />
            </div>
          </div>

          {/* Content */}
          <div className="flex-1 flex flex-col min-h-0">
            {/* Audio Player */}
            <div className="mb-4 flex-shrink-0">
              {exercise && <AudioPlayer audioText={exercise.sentence} />}
            </div>

            {/* Answer / Feedback */}
            <div className="flex-1 min-h-0 overflow-auto">
              {!answer.submitted ? (
                <AnswerInput
                  onSubmit={handleSubmitAnswer}
                  disabled={answer.submitted || loading}
                />
              ) : (
                <FeedbackCard
                  isCorrect={answer.isCorrect ?? false}
                  userAnswer={answer.userAnswer ?? ""}
                  correctAnswer={answer.corrected_sentence ?? ""}
                  explanation={answer.feedback ?? ""}
                  onNext={handleNext}
                  isLastQuestion={currentIndex === TOTAL_EXERCISES}
                />
              )}
            </div>
          </div>

          {/* Navigation Buttons */}
          <div className="mt-4 flex justify-between flex-shrink-0">
            <Button
              onClick={handlePrevious}
              disabled={currentIndex === 1}
              variant="outline"
              size="lg"
            >
              <ChevronLeft className="w-5 h-5 mr-2" />
              Previous
            </Button>

            <Button
              onClick={handleNext}
              disabled={currentIndex === TOTAL_EXERCISES}
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
