def feedback_prompt(image_context,audio_text):
    f"""
        You are an expert evaluator in communication skills.
        Evaluate the following based on the provided image context and audio text.

        Image context: {image_context}
        Audio Text: {audio_text}

        evaluate the audio_text only if it matches the image context.
        If not related, reduce the overall score significantly.

        Evaluate based on:
        Clarity of speech,
        Professionalism,
        Tone,
        Grammar,
        Vocabulary,
        Fluency,
        Coherence,
        Accuracy,
        Overall Score (0–5),
        Summary,
        Detailed Feedback

        Important rules:
        - If too short or <1 min → reduce score
        - If lacking depth → reduce score
        - Must strictly relate to image
        - Output only JSON

        Example:
        {{
          "Clarity of speech": "... Score: 4/5",
          "Overall Score": "3/5"
        }}
        """

def relevance_prompt(transcript: str):
    f"""
    You are a relevance evaluator.
    Determine if the spoken description matches the image context.

    Transcript:
    {transcript}

    Give score 0–5 and reason.

    Return JSON:
    {{
     "relevance": {{
       "score": int,
       "reason": ""
     }}
    }}
    """