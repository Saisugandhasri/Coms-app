import { useState, useRef, useEffect } from "react";
import { Play, Pause, RotateCcw, Volume2 } from "lucide-react";
import { Button } from "./ui/button";

interface AudioPlayerProps {
  audioText: string;
}

export function AudioPlayer({ audioText }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false); // controls Pause/Resume
  const [progress, setProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [hasPlayed, setHasPlayed] = useState(false); // controls Play/Replay

  /* -----------------------------
     Reset when sentence changes
  ------------------------------ */
  useEffect(() => {
    if (audioUrl) URL.revokeObjectURL(audioUrl);
    setAudioUrl(null);
    setIsPlaying(false);
    setProgress(0);
    setHasPlayed(false); // reset Play/Replay button for new question
  }, [audioText]);

  /* -----------------------------
     Cleanup on unmount
  ------------------------------ */
  useEffect(() => {
    return () => {
      if (audioUrl) URL.revokeObjectURL(audioUrl);
    };
  }, [audioUrl]);

  /* -----------------------------
     Fetch TTS Audio
  ------------------------------ */
  const loadAudio = async () => {
    if (audioUrl) return;

    setLoading(true);
    const res = await fetch("http://localhost:8000/api/exercise/tts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: audioText }),
    });

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    setAudioUrl(url);
    setLoading(false);
  };

  /* -----------------------------
     Play / Replay / Pause / Resume
  ------------------------------ */
  const handlePlayReplay = async () => {
    if (!audioUrl) {
      await loadAudio();
      if (!audioRef.current) return;

      // Play audio when it is ready
      audioRef.current.oncanplay = () => {
        audioRef.current!.currentTime = 0;
        audioRef.current!.play();
        setIsPlaying(true);
        audioRef.current!.oncanplay = null; // clean up
      };
      return;
    }

    if (audioRef.current) {
      audioRef.current.currentTime = 0;
      audioRef.current.play();
      setIsPlaying(true);
    }
  };

  const handlePauseResume = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.play();
      setIsPlaying(true);
    }
  };

  /* -----------------------------
     Progress tracking
  ------------------------------ */
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateProgress = () => {
      setProgress(audio.currentTime / audio.duration || 0);
    };

    const handleEnded = () => {
      setIsPlaying(false);
      setProgress(0);
    };

    audio.addEventListener("timeupdate", updateProgress);
    audio.addEventListener("ended", handleEnded);

    return () => {
      audio.removeEventListener("timeupdate", updateProgress);
      audio.removeEventListener("ended", handleEnded);
    };
  }, [audioUrl]);

  return (
    <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
      <div className="flex items-center gap-3 mb-4">
        <Volume2 className="w-5 h-5 text-blue-600" />
        <h3>Listen to the Audio</h3>
      </div>

      <div className="space-y-4">
        {/* Progress bar */}
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-100"
            style={{ width: `${progress * 100}%` }}
          />
        </div>

        {/* Controls */}
        <div className="flex gap-2 justify-center">
          {/* Left button: Play / Replay */}
          <Button
            onClick={handlePlayReplay}
            size="lg"
            className="bg-blue-600 hover:bg-blue-700"
            disabled={loading}
          >
            {hasPlayed ? <RotateCcw className="mr-2" /> : <Play className="mr-2" />}
            {hasPlayed ? "Replay" : "Play"}
          </Button>

          {/* Right button: Pause / Resume */}
          <Button
            onClick={handlePauseResume}
            variant="outline"
            size="lg"
            disabled={loading || !audioUrl}
          >
            {isPlaying ? <Pause className="mr-2" /> : <Play className="mr-2" />}
            {isPlaying ? "Pause" : "Resume"}
          </Button>
        </div>

        {loading && (
          <p className="text-center text-sm text-gray-500">
            Generating audio…
          </p>
        )}

        {/* Audio element */}
        <audio
          ref={audioRef}
          src={audioUrl}
          onPlay={() => setHasPlayed(true)} // Only set hasPlayed when audio actually plays
        />
      </div>
    </div>
  );
}
