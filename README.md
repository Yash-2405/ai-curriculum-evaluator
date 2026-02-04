# AI Curriculum Generator + Evaluator (V2 FULL)

This is a Curriculum Engineer aligned MVP project:

✅ Dynamic assignment generation using **Gemini Free API**  
✅ Topics: SQL, Python, ETL, GenAI  
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
GEMINI_API_KEY = "PASTE_YOUR_KEY_HERE"
```

### 3. Run Server
```bash
python app.py
```

Open browser:

http://127.0.0.1:5000

---

## Demo Flow
1. Select topic → Generate Assignment  
2. If SQL topic → Write query → Evaluate  
3. Get score + feedback instantly
