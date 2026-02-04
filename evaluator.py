import sqlite3
import json
from groq import Groq


GROQ_API_KEY = "YOUR_GROQ_API"

client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"


# =====================================================
# ✅ SQL EXECUTION EVALUATOR
# =====================================================

def run_query(schema_sql, seed_sql, query_sql):

    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    cur.executescript(schema_sql)
    cur.executescript(seed_sql)

    cur.execute(query_sql)

    return cur.fetchall()


def evaluate_sql(student_sql, expected_sql, schema_sql, seed_sql):

    try:
        student_out = run_query(schema_sql, seed_sql, student_sql)
    except Exception as e:
        return {"status": "fail", "score": 0, "error": str(e)}

    expected_out = run_query(schema_sql, seed_sql, expected_sql)

    if student_out == expected_out:
        return {
            "status": "success",
            "score": 10,
            "feedback": "Perfect SQL output match!",
            "output": student_out
        }

    return {
        "status": "partial",
        "score": 5,
        "feedback": "Query executed but output differs.",
        "your_output": student_out,
        "expected_output": expected_out
    }


# =====================================================
# ✅ UNIVERSAL LLM GRADER (Python/ETL/GenAI)
# =====================================================

def llm_grade_assignment(assignment, rubric, student_answer):

    prompt = f"""
You are a strict curriculum evaluator.

Grade ONLY based on rubric requirements.

Assignment:
{assignment}

Rubric Requirements:
{rubric}

Student Answer:
{student_answer}

Return STRICT JSON:

{{
  "score": 0-10,
  "feedback": "...",
  "strengths": ["..."],
  "missing": ["..."]
}}
"""

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = completion.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except:
        return {
            "score": 0,
            "feedback": "LLM grading failed (invalid JSON).",
            "strengths": [],
            "missing": ["Parsing error"]
        }
