import json
from groq import Groq

# ✅ Paste Groq API Key
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"

client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"


def llm_grade_assignment(assignment, rubric, student_answer):
    """
    Universal evaluator: uses Groq model to grade any answer
    against any rubric.
    """

    prompt = f"""
You are an expert curriculum evaluator.

Grade the student's answer.

Assignment:
{assignment}

Rubric Requirements:
{rubric}

Student Answer:
{student_answer}

Return STRICT JSON only:

{{
  "score": integer from 0 to 10,
  "feedback": "short explanation",
  "strengths": ["point1","point2"],
  "missing": ["missing1","missing2"]
}}
"""

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = completion.choices[0].message.content.strip()

    try:
        return json.loads(response_text)
    except:
        return {
            "score": 0,
            "feedback": "Evaluation failed (invalid JSON from model).",
            "strengths": [],
            "missing": ["Could not parse response"]
        }
