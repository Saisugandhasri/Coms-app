import { BrowserRouter, Routes, Route } from "react-router-dom";
import AppTense from "./app/AppTense";
import AppCorrect from "./app/AppCorrect";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppTense />} />
        <Route path="/convert-tense" element={<AppTense />} />
        <Route path="/correct-sentence" element={<AppCorrect />} />
      </Routes>
    </BrowserRouter>
  );
}

