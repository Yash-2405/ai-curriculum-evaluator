import json
import re
from groq import Groq

# ✅ Paste Groq API Key here
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.1-8b-instant"


def generate_assignment(topic="SQL"):

    # ✅ Strict Prompt: JSON ONLY
    if topic == "SQL":
        prompt = f"""
Return ONLY valid JSON. No markdown. No extra text.

Format:

{{
  "assignment": "...",
  "schema_sql": "CREATE TABLE ...;",
  "seed_sql": "INSERT INTO ...;",
  "expected_answer": "SELECT ...;",
  "rubric": ["step1","step2","step3"]
}}

Rules:
- schema_sql must include CREATE TABLE
- seed_sql must include 5–8 INSERT rows
- expected_answer must run correctly
"""

    else:
        prompt = f"""
Return ONLY valid JSON. No markdown. No explanation.

Format:

{{
  "assignment": "...",
  "schema_sql": "",
  "seed_sql": "",
  "expected_answer": "",
  "rubric": ["requirement1","requirement2","requirement3"]
}}

Topic: {topic}

Rules:
- rubric must contain 5–7 grading requirements
"""

    # ✅ Call Groq
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = completion.choices[0].message.content.strip()

    # ✅ BULLETPROOF JSON EXTRACTION
    try:
        # Extract first {...} block only
        match = re.search(r"\{.*\}", raw_output, re.DOTALL)

        if not match:
            raise ValueError("No JSON object found in response")

        json_text = match.group()
        data = json.loads(json_text)

    except Exception as e:
        # ✅ Emergency fallback
        data = {
            "assignment": raw_output,
            "schema_sql": "",
            "seed_sql": "",
            "expected_answer": "",
            "rubric": ["Model output was invalid JSON"]
        }

    return (
        data.get("assignment", ""),
        data.get("schema_sql", ""),
        data.get("seed_sql", ""),
        data.get("expected_answer", ""),
        data.get("rubric", [])
    )
