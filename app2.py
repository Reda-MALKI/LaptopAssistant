from flask import Flask, request, render_template, jsonify
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import SQLDatabase

app = Flask(__name__)


API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY")


llm = ChatOpenAI(
    openai_api_key=API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openai/gpt-4o-mini",
    temperature=0.3,
)


translate_prompt = PromptTemplate.from_template("""
Translate this Moroccan Darija/Arabic question to clear English.
Only return the English translation.

Darija: {question}
English:
""")

translate_chain = translate_prompt | llm


def translate_to_english(darija_text):
    result = translate_chain.invoke({"question": darija_text})
    return result.content.strip()


sql_prompt = PromptTemplate.from_template("""
You are a SQL expert.

Database schema:
{schema}

Write a SQL query to answer:
{question}

IMPORTANT:
- Return ONLY SQL
- No markdown
- No explanations
""")

sql_chain = sql_prompt | llm


def generate_sql_query(question_en, table_info):
    result = sql_chain.invoke({
        "schema": table_info,
        "question": question_en
    })
    return result.content.strip().replace("```", "").strip()



darija_prompt = PromptTemplate.from_template("""
You are a helpful assistant responding in Moroccan Darija (Latin script).

User question: {question}
SQL query executed: {sql}
Database result: {result}

Respond clearly in Darija.
""")

darija_chain = darija_prompt | llm


def generate_darija_response(question, sql_result, sql_query):
    result = darija_chain.invoke({
        "question": question,
        "sql": sql_query,
        "result": sql_result
    })
    return result.content.strip()



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_question = data.get("question", "").strip()

    if not user_question:
        return jsonify({"answer": "kteb shi so2al bach njawbek."})

    try:
        print("=" * 50)
        print("Original:", user_question)

        # Step 1: Translate
        question_en = translate_to_english(user_question)
        print("English:", question_en)

        # Step 2: Connect to DB
        db = SQLDatabase.from_uri("sqlite:///db.sqlite3")
        schema = db.get_table_info()

        db = SQLDatabase.from_uri("sqlite:///db.sqlite3")
        print(db.get_usable_table_names())

        # Step 3: Generate SQL
        sql_query = generate_sql_query(question_en, schema)
        print("SQL : ----------!!!!! this is the SQL query : ", sql_query)

        # Step 4: Execute SQL
        sql_result = db.run(sql_query)
        print("Result:", sql_result)

        # Step 5: Generate Darija Answer
        darija_response = generate_darija_response(
            user_question,
            sql_result,
            sql_query
        )

        print("Darija:", darija_response)
        print("=" * 50)

        return jsonify({
            "answer": darija_response,
            "sql": sql_query,
            "raw_result": str(sql_result)
        })

    except Exception as e:
        return jsonify({"answer": f"smh liya, kayn moshkil: {str(e)}"})



if __name__ == "__main__":
    print("Running on http://127.0.0.1:5000")
    app.run(debug=True)
