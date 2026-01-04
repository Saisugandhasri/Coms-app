import { useState, useRef } from 'react';
import { Mic, Type, Send } from 'lucide-react';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

interface AnswerInputProps {
  onSubmit: (answer: string | Blob, isAudio: boolean) => void;

  disabled?: boolean;
}

export function AnswerInput({ onSubmit, disabled }: AnswerInputProps) {
  const [textAnswer, setTextAnswer] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [audioAnswer, setAudioAnswer] = useState('');
  const [activeTab, setActiveTab] = useState<'text' | 'audio'>('text');

  /* 🔥 NEW: real audio recording state */
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const recordedAudioRef = useRef<Blob | null>(null);

  const handleTextSubmit = () => {
    if (textAnswer.trim()) {
      onSubmit(textAnswer.trim(), false);
    }
  };

  /* 🔥 FIXED: real microphone recording */
  const handleRecordToggle = async () => {
    if (!isRecording) {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };

      recorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: 'audio/webm',
        });

        recordedAudioRef.current = audioBlob;
        setAudioAnswer('Audio recorded successfully');
        stream.getTracks().forEach(track => track.stop());

      };

      recorder.start();
      setIsRecording(true);
    } else {
      mediaRecorderRef.current?.stop();
      setIsRecording(false);
    }
  };

  /* 🔥 Submit audio (real audio, not fake text) */
  const handleAudioSubmit = () => {
    if (recordedAudioRef.current) {
      onSubmit(recordedAudioRef.current, true);
    }
  };

  return (
    <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
      <h3 className="mb-4">Your Answer</h3>

      <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as 'text' | 'audio')}>
        <TabsList className="grid w-full grid-cols-2 mb-4">
          <TabsTrigger value="text" className="flex items-center gap-2">
            <Type className="w-4 h-4" />
            Text
          </TabsTrigger>
          <TabsTrigger value="audio" className="flex items-center gap-2">
            <Mic className="w-4 h-4" />
            Audio
          </TabsTrigger>
        </TabsList>

        <TabsContent value="text" className="space-y-4">
          <Textarea
            placeholder="Type the corrected sentence here..."
            value={textAnswer}
            onChange={(e) => setTextAnswer(e.target.value)}
            className="min-h-[100px]"
            disabled={disabled}
          />
          <Button
            onClick={handleTextSubmit}
            disabled={!textAnswer.trim() || disabled}
            className="w-full bg-blue-600 hover:bg-blue-700"
            size="lg"
          >
            <Send className="w-5 h-5 mr-2" />
            Submit Answer
          </Button>
        </TabsContent>

        <TabsContent value="audio" className="space-y-4">
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 flex flex-col items-center justify-center min-h-[100px]">
            {isRecording ? (
              <div className="text-center">
                <div className="w-16 h-16 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-3 animate-pulse">
                  <Mic className="w-8 h-8 text-white" />
                </div>
                <p className="text-red-600">Recording...</p>
              </div>
            ) : audioAnswer ? (
              <div className="text-center">
                <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Mic className="w-8 h-8 text-white" />
                </div>
                <p className="text-green-600">Recording captured</p>
              </div>
            ) : (
              <div className="text-center">
                <Mic className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                <p className="text-gray-500">Click the button below to start recording</p>
              </div>
            )}
          </div>

          <div className="flex gap-2">
            <Button
              onClick={handleRecordToggle}
              variant={isRecording ? 'destructive' : 'outline'}
              className="flex-1"
              size="lg"
              disabled={disabled}
            >
              <Mic className="w-5 h-5 mr-2" />
              {isRecording ? 'Stop Recording' : audioAnswer ? 'Re-record' : 'Start Recording'}
            </Button>
          </div>

          {audioAnswer && (
            <Button
              onClick={handleAudioSubmit}
              disabled={disabled}
              className="w-full bg-blue-600 hover:bg-blue-700"
              size="lg"
            >
              <Send className="w-5 h-5 mr-2" />
              Submit Answer
            </Button>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
