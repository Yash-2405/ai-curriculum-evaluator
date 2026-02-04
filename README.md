# AI Curriculum Generator + Evaluator (V2 FULL)

This is a Curriculum Engineer aligned MVP project:

✅ Dynamic assignment generation using **GROK API**  
✅ Topics: SQL, Python + Data Cleaning  
✅ SQL Evaluation Agent with scoring + feedback  
✅ Tool execution using SQLite  

---

## Setup

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Add Gemini API Key
Open `generator.py`

Replace:

```python
GROK_API_KEY = "PASTE_YOUR_KEY_HERE"
```

### 3. Run Server
```bash
python app.py
```

---

## Demo Flow
1. Select topic → Generate Assignment  
2. If SQL topic → Write query → Evaluate  
3. Get score + feedback instantly

---

## Future Scope

1. Support for ETL + GenAI workflows

2. Secure Python code execution sandbox

3. Adaptive rubric extraction
