from flask import Flask, request, jsonify, render_template, session

from generator import generate_assignment
from evaluator import evaluate_sql, llm_grade_assignment

app = Flask(__name__)
app.secret_key = "curriculum_secret_key"


@app.route("/")
def home():
    return render_template("index.html")


# =====================================================
# ✅ GENERATE ASSIGNMENT (ALL TOPICS)
# =====================================================

@app.route("/generate", methods=["POST"])
def gen():
    topic = request.json.get("topic", "SQL")

    assignment, schema_sql, seed_sql, expected_sql, rubric = generate_assignment(topic)

    # Store in session
    session["topic"] = topic
    session["assignment"] = assignment
    session["schema_sql"] = schema_sql
    session["seed_sql"] = seed_sql
    session["expected_sql"] = expected_sql
    session["rubric"] = rubric

    return jsonify({
        "topic": topic,
        "assignment": assignment,
        "rubric": rubric
    })


# =====================================================
# ✅ EVALUATE ANSWER (SQL + NON-SQL)
# =====================================================

@app.route("/evaluate", methods=["POST"])
def eval_query():
    data = request.get_json()

    topic = session.get("topic", "SQL")
    student_answer = data.get("answer", "")

    # ✅ SQL Execution Mode
    if topic == "SQL":
        return jsonify(
            evaluate_sql(
                student_answer,
                session.get("expected_sql", ""),
                session.get("schema_sql", ""),
                session.get("seed_sql", "")
            )
        )

    # ✅ LLM Grading Mode
    return jsonify(
        llm_grade_assignment(
            session.get("assignment", ""),
            session.get("rubric", []),
            student_answer
        )
    )


if __name__ == "__main__":
    app.run(debug=True)
