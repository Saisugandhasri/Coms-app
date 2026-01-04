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

export default function AppCorrect() {
  const TOTAL_EXERCISES = 5;

  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [exerciseId, setExerciseId] = useState<string | null>(null);

  const createEmptyAnswers = (): AnswerState[] =>
    Array.from({ length: TOTAL_EXERCISES }, () => ({
      userAnswer: null,
      isCorrect: null,
      submitted: false,
    }));

  const [answers, setAnswers] = useState<AnswerState[]>(createEmptyAnswers());
  const [loading, setLoading] = useState(false);

  const [currentIndex, setCurrentIndex] = useState(1);
  const [answeredCount, setAnsweredCount] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);
  const [answeredMap, setAnsweredMap] = useState<Record<number, boolean>>({});

  const currentExercise = exercises[currentIndex - 1] ?? null;
  const currentAnswer = answers[currentIndex - 1] ?? {
    userAnswer: null,
    isCorrect: null,
    submitted: false,
  };

  /* -----------------------------
     Fetch Exercises
  ------------------------------ */
  const startExercise = async () => {
    try {
      setLoading(true);

      const res = await fetch(
        "http://localhost:8000/api/exercise/correct/start",
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

      if (isAudio) {
        const formData = new FormData();
        formData.append("exercise_id", exerciseId);
        formData.append("sentence", currentExercise.sentence);
        formData.append("audio_file", userAnswer as Blob);

        res = await fetch(
          "http://localhost:8000/api/exercise/correct/answer/audio",
          {
            method: "POST",
            body: formData,
          }
        );
      } else {
        res = await fetch(
          "http://localhost:8000/api/exercise/correct/answer/text",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              exercise_id: exerciseId,
              sentence: currentExercise.sentence,
              user_answer: userAnswer,
            }),
          }
        );
      }

      if (!res.ok) throw new Error("Failed to submit answer");

      const data = await res.json();

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

      setAnsweredMap((prev) => {
        if (prev[currentIndex]) return prev;

        setAnsweredCount((c) => c + 1);
        if (data.is_correct) setCorrectCount((c) => c + 1);

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
     UI
  ------------------------------ */
  return (
    <div className="h-screen bg-gray-50 flex flex-col overflow-hidden">
      <main className="flex-1 flex flex-col">
        <div className="max-w-4xl mx-auto px-6 py-6 w-full flex flex-col h-full">

          <div className="mb-6">
            <h1 className="text-3xl mb-2">Correct the Sentence</h1>
            <p className="text-gray-600">
              The sentence below has one grammatical mistake. Correct it.
            </p>
          </div>

          <div className="mb-4">
            {currentExercise && (
              <AudioPlayer audioText={currentExercise.sentence} />
            )}
          </div>

          <div className="flex-1 overflow-auto">
            {!currentAnswer.submitted ? (
              <AnswerInput
                onSubmit={handleSubmitAnswer}
                disabled={loading}
              />
            ) : (
              <FeedbackCard
                isCorrect={currentAnswer.isCorrect}
                userAnswer={currentAnswer.userAnswer ?? ""}
                correctAnswer={currentAnswer.corrected_sentence ?? ""}
                explanation={currentAnswer.feedback ?? ""}
                onNext={() => setCurrentIndex((i) => i + 1)}
                isLastQuestion={currentIndex === TOTAL_EXERCISES}
              />
            )}
          </div>

        </div>
      </main>
    </div>
  );
}
