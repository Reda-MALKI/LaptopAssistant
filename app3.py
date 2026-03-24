from flask import Flask

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import SQLDatabase

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("No API key is set , set one api key alright")
else:
    print("Alright the api key is set and well loaded")

llm = ChatOpenAI(
    openai_api_key = API_KEY,
    openai_api_base = "https://openrouter.ai/api/v1",
    model_name = "gpt-4o-mini",
    temperature = 0.6
)

print("---------------Now the Database Stuff--------------")

question = PromptTemplate.from_template("""
    Translate this {question} into french.
""")

translation = question | llm

def generate_translation(question):
    result = translation.invoke({"question" : question})
    return result.content.strip()

query = PromptTemplate.from_template("""
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

query_chain = query | llm

def generate_sql_query(schema , question):
    result = query_chain.invoke({
        "schema" : schema,
        "question" : question
    })
    return result.content.strip()

response = PromptTemplate.from_template(""" 
    OK now you have these three things :
    Question : {question}
    SQL query  : {query}
    Answer : {answer}
    Now generate the answer in french no error alright
                                        """)

response_chain = response | llm

def generate_response(question , query , answer):
    result = response_chain.invoke({
        "question" : question,
        "query" : query,
        "answer" : answer
    })
    return result.content.strip()

question = "How many clients are there : "

result = generate_translation(question)
print(result)

database = SQLDatabase.from_uri("sqlite:///db.sqlite3")

if database:
    print("Database successfully loaded")

schema = database.get_table_info()
print(schema)

query = generate_sql_query(schema , result)
print("The SQL query is  :  " , query)

resulted_search = database.run(query)

print("The resulted search is  :  ", resulted_search)

response = generate_response(question , query  , resulted_search)

print(response)