from flask import Flask, request, render_template, jsonify
import os
import requests
from langchain_community.utilities import SQLDatabase

app = Flask(__name__)

# -----------------------------
# 1. Load OpenRouter API Key
# -----------------------------
DEEPSEEK_KEY = os.getenv("OPENROUTER_API_KEY")
if not DEEPSEEK_KEY:
    raise ValueError("ERROR: Missing OPENROUTER_API_KEY. Use: setx OPENROUTER_API_KEY 'your_key'")

# -----------------------------
# 2. OpenRouter API call
# -----------------------------
def call_openrouter(prompt, temperature=0.3):
    """Call OpenRouter API and return text"""
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": 500
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            # Some OpenRouter responses return "text" or "message" depending on model
            choice = data["choices"][0]
            if "text" in choice:
                return choice["text"].strip()
            elif "message" in choice and "content" in choice["message"]:
                return choice["message"]["content"].strip()
        print(f"Unexpected API response: {data}")
        return None
    except Exception as e:
        print(f"OpenRouter API Error: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response text: {e.response.text}")
        return None

# -----------------------------
# 3. Translate Darija to English
# -----------------------------
def translate_to_english(darija_text):
    prompt = f"""Translate this Moroccan Darija/Arabic question to clear English.
Only return the English translation, nothing else.

Darija: {darija_text}
English:"""
    translation = call_openrouter(prompt, temperature=0.1)
    if translation:
        return translation.replace("English:", "").strip()
    return darija_text

# -----------------------------
# 4. Generate SQL Query
# -----------------------------
def generate_sql_query(question_en, table_info):
    prompt = f"""You are a SQL expert. Given this database schema:

{table_info}

Write a SQL query to answer: {question_en}

IMPORTANT:
- Return ONLY the SQL query
- No explanations, no markdown, no backticks
- Just plain SQL

SQL Query:"""
    sql_query = call_openrouter(prompt, temperature=0.1)
    if not sql_query:
        return None
    sql_query = sql_query.strip()
    for tag in ["```sql", "```", "SQL Query:"]:
        if tag in sql_query:
            sql_query = sql_query.split(tag)[-1].strip()
    sql_query = sql_query.replace("SELECT SELECT", "SELECT").strip(";").strip()
    return sql_query

# -----------------------------
# 5. Generate Darija Response
# -----------------------------
def generate_darija_response(question, sql_result, sql_query):
    prompt = f"""You are a helpful assistant that responds in Moroccan Darija (Moroccan Arabic dialect).

User question: {question}
SQL query executed: {sql_query}
Result from database: {sql_result}

Respond in Moroccan Darija (Latin script):
- Use Moroccan words like: chhal, kayn, dyal, li, wash, 3andna, hna
- Be clear and helpful
- If result is a number, explain it simply
- If result is a list, organize it clearly
- Keep response direct and natural

Your Darija response (in Latin script):"""
    response = call_openrouter(prompt, temperature=0.6)
    if not response:
        if isinstance(sql_result, (int, float)):
            return f"3andna {sql_result}"
        return f"l9it: {sql_result}"
    return response.strip()

# -----------------------------
# 6. Flask Routes
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_question = data.get("question", "").strip()
    if not user_question:
        return jsonify({"answer": "makaynsh so2al. kteb shi haja bach njawbek."})

    try:
        print(f"\n{'='*60}")
        print(f"Original question: {user_question}")
        question_en = translate_to_english(user_question)
        print(f"English translation: {question_en}")

        # -----------------------------
        # Reconnect to DB on each request
        # -----------------------------
        db = SQLDatabase.from_uri("sqlite:///db.sqlite3")
        table_info = db.get_table_info()
        sql_query = generate_sql_query(question_en, table_info)
        if not sql_query:
            return jsonify({"answer": "smh liya, ma9dertch nfhem so2al. hawel tsigo b tariqa okhra."})

        print(f"Generated SQL: {sql_query}")
        sql_result = db.run(sql_query)
        print(f"Result: {sql_result}")

        darija_response = generate_darija_response(user_question, sql_result, sql_query)
        print(f"Darija response: {darija_response}")
        print(f"{'='*60}\n")

        return jsonify({
            "answer": darija_response,
            "sql": sql_query,
            "raw_result": str(sql_result)
        })

    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
        if "no such table" in error_msg.lower():
            return jsonify({"answer": "smh liya, tabla mal9itha. ta2aked mn database."})
        elif "syntax error" in error_msg.lower():
            return jsonify({"answer": "kayn ghalat f SQL. hawel tsawel b tariqa okhra."})
        elif "no such column" in error_msg.lower():
            return jsonify({"answer": "l field li tlebti makaynsh. shuf shno 3andek f tabla."})
        else:
            return jsonify({"answer": f"smh liya, moshkil ti9ni: {error_msg}"})

# -----------------------------
# 7. Launch Server
# -----------------------------
if __name__ == "__main__":
    print("RAG Demo running on http://127.0.0.1:5000")
    print(f"API Key: {'Loaded' if DEEPSEEK_KEY else 'Missing'}")

    # Print database info at startup
    try:
        db = SQLDatabase.from_uri("sqlite:///db.sqlite3")
        tables = db.get_usable_table_names()
        print(f"Tables: {tables}")
        for table in tables:
            print(f"\nStructure of '{table}':")
            print(db.get_table_info([table]))
            try:
                sample = db.run(f"SELECT * FROM {table} LIMIT 3")
                print(f"Sample data: {sample}")
            except:
                pass
    except Exception as e:
        print(f"Database error: {e}")

    print("\nReady! Try asking questions in Darija...\n")
    app.run(debug=True)
