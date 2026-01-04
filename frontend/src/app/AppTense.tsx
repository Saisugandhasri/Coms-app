import { useState, useEffect } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { AudioPlayer } from "./components/AudioPlayer";
import { AnswerInput } from "./components/AnswerInput";
import { FeedbackCard } from "./components/FeedbackCard";
import { Button } from "./components/ui/button";


/* -----------------------------
   Types
------------------------------ */

interface Exercise {
  sentence: string;
  target_tense: string;
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
  const TOTAL_EXERCISES = 5;

  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [exerciseId, setExerciseId] = useState<string | null>(null);

  // ✅ FIX: create independent answer objects
  const createEmptyAnswers = (): AnswerState[] =>
    Array.from({ length: TOTAL_EXERCISES }, () => ({
      userAnswer: null,
      isCorrect: null,
      submitted: false,
    }));

  const [answers, setAnswers] = useState<AnswerState[]>(createEmptyAnswers());

  const [loading, setLoading] = useState(false);

  // UI counters
  const [currentIndex, setCurrentIndex] = useState(1);
  const [answeredCount, setAnsweredCount] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);

  // Track answered questions safely
  const [answeredMap, setAnsweredMap] = useState<Record<number, boolean>>({});

  // ✅ current exercise derived from array
  const currentExercise = exercises[currentIndex - 1] ?? null;
  const currentAnswer =
    answers[currentIndex - 1] ?? {
      userAnswer: null,
      isCorrect: null,
      submitted: false,
    };

  /* -----------------------------
     Fetch Exercises (ONCE)
  ------------------------------ */
  const startExercise = async () => {
    try {
      setLoading(true);

      const res = await fetch(
        "http://localhost:8000/api/exercise/tense/start",
        { method: "POST" }
      );

      if (!res.ok) throw new Error("Failed to start exercise");

      const data = await res.json();

      setExerciseId(data.exercise_id);
      setExercises(data.questions);

      setCurrentIndex(1);
      setAnsweredCount(0);
      setCorrectCount(0);
      setAnsweredMap({});
      setAnswers(createEmptyAnswers());

    } catch (err) {
      console.error(err);
      alert("Failed to load exercises");
    } finally {
      setLoading(false);
    }
  };

  // ✅ fetch ONLY ONCE
  useEffect(() => {
    startExercise();
  }, []);

  /* -----------------------------
     Submit Answer
  ------------------------------ */
  const handleSubmitAnswer = async (
    userAnswer: string | Blob,
    isAudio: boolean
  ) => {
    if (!currentExercise || !exerciseId) return;

    try {
      setLoading(true);
      let res: Response;

      /* -----------------------------
         AUDIO SUBMISSION
      ------------------------------ */
      if (isAudio) {
        const formData = new FormData();

        formData.append("exercise_id", exerciseId);
        formData.append("sentence", currentExercise.sentence);
        formData.append("target_tense", currentExercise.target_tense);
        formData.append("audio_file", userAnswer as Blob);


        res = await fetch(
          "http://localhost:8000/api/exercise/tense/answer/audio",
          {
            method: "POST",
            body: formData,
          }
        );
      }

      /* -----------------------------
         TEXT SUBMISSION
      ------------------------------ */
      else {
        res = await fetch(
          "http://localhost:8000/api/exercise/tense/answer/text",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              exercise_id: exerciseId,
              sentence: currentExercise.sentence,
              target_tense: currentExercise.target_tense,
              user_answer: userAnswer,
            }),
          }
        );
      }

      if (!res.ok) throw new Error("Failed to submit answer");

      const data = await res.json();

      // ✅ FIX: update only current index safely
      setAnswers((prev) => {
        const updated = [...prev];
        updated[currentIndex - 1] = {
          userAnswer: isAudio
            ? data.transcribed_text
            : (userAnswer as string),
          isCorrect: data.is_correct,
          submitted: true,
          feedback: data.feedback,
          corrected_sentence: data.corrected_sentence,
        };
        return updated;
      });

      // ✅ Count answered question ONLY ONCE
      setAnsweredMap((prev) => {
        if (prev[currentIndex]) return prev;

        setAnsweredCount((c) => c + 1);
        if (data.is_correct) {
          setCorrectCount((c) => c + 1);
        }

        return { ...prev, [currentIndex]: true };
      });

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
                  width: `${(answeredCount / TOTAL_EXERCISES) * 100}%`,

                }}
              />
            </div>
          </div>

          {/* Content */}
          <div className="flex-1 flex flex-col min-h-0">
            {/* Audio Player */}
            <div className="mb-4 flex-shrink-0">
              {currentExercise && (
                <AudioPlayer audioText={currentExercise.sentence} />
              )}
            </div>

            {/* Target Tense */}
              {currentExercise && (
                <div className="mb-4 text-sm text-gray-700">
                  Convert the given question into :{" "}
                  <span className="font-semibold text-blue-700">
                    {currentExercise.target_tense}
                  </span>
                </div>
              )}


            {/* Answer / Feedback */}
            <div className="flex-1 min-h-0 overflow-auto">
              {!currentAnswer.submitted ? (
                <AnswerInput
                  onSubmit={handleSubmitAnswer}
                  disabled={currentAnswer.submitted || loading}
                />
              ) : (
                <FeedbackCard
                  isCorrect={currentAnswer.isCorrect}
                  userAnswer={currentAnswer.userAnswer ?? ""}
                  correctAnswer={currentAnswer.corrected_sentence ?? ""}
                  explanation={currentAnswer.feedback ?? ""}
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
              disabled={
                currentIndex === TOTAL_EXERCISES
              }
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
