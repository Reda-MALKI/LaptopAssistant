## LAPTOPASSISTANT – AI CHATBOT FOR DATABASE QUERYING
### 🧠 OVERVIEW

#### LaptopAssistant is an intelligent AI-powered chatbot that allows users to query a database using natural language (Moroccan Darija, Arabic, or English).

#### Instead of writing SQL queries manually, users can simply ask questions like:

“chhal mn client kayn?”
“chnohoma les pcs li 3ndkom?”

👉 The system automatically:

Translates the question
Generates a SQL query
Executes it on the database
Returns a human-like response in Darija
⚙️ PROJECT ARCHITECTURE & FILE VERSIONS

#### This project includes three different implementations of the same idea, each with a different level of control and abstraction:

🔹 Direct API version (manual control – production ready)
🔹 LangChain version (modular & clean)
🔹 Standalone version (testing & debugging)
⚙️ VERSION 1 – app.py (ADVANCED – DIRECT API CONTROL)
🔥 Description

This is the most advanced and production-ready version.

It directly interacts with the LLM using HTTP requests via OpenRouter, giving full control over:

Prompt engineering
Output formatting
Error handling
#### 🧩 Key Features
Direct API calls using requests
Custom prompt engineering
SQL cleaning & sanitization
Strong error handling (SQL errors, missing tables, etc.)
Darija response generation with structured rules
#### ⚙️ Pipeline
Darija Question
   ↓
Translate → English
   ↓
Generate SQL (LLM)
   ↓
Execute SQL (SQLite)
   ↓
Generate Darija Response
#### 💡 Why this version matters

✅ Full control over LLM
✅ More robust and reliable
✅ Better suited for production

#### ⚙️ VERSION 2 – app.py (LANGCHAIN IMPLEMENTATION)
#### 🔥 Description

This version uses LangChain to simplify the pipeline using prompt chaining.

#### 🧩 Key Features
Uses ChatOpenAI
Uses PromptTemplate
Chain-based architecture (prompt | llm)
Cleaner and more modular code
#### ⚙️ Pipeline
Darija Question
   ↓
Translation Chain
   ↓
SQL Generation Chain
   ↓
Database Execution
   ↓
Darija Response Chain
### 💡 Pros & Cons
#### ✅ Pros
Clean structure
Fast development
Easy to extend
#### ❌ Cons
Less control over LLM
Harder debugging
More hallucination risk

### 👉 Ideal for prototyping and learning

#### ⚙️ VERSION 3 – app.py (STANDALONE PIPELINE)
#### 🔥 Description

This version is a script-based pipeline (no Flask API).

It is used for testing and understanding how the system works step-by-step.

#### 🧩 Key Features
Runs in terminal
Step-by-step pipeline execution
Debug-friendly
Uses French for output (variation)
#### ⚙️ Pipeline
Question
   ↓
Translate → French
   ↓
Generate SQL
   ↓
Execute Query
   ↓
Generate Response
#### 💡 Why this version is useful

✅ Debugging
✅ Testing prompts
✅ Understanding pipeline logic

#### 🆚 COMPARISON OF THE 3 VERSIONS
Feature	Direct API	LangChain	Standalone
Control 🔥	✅ High	❌ Medium	✅ High
Simplicity	⚠️ Medium	✅ High	✅ High
Debugging	✅ Easy	❌ Harder	✅ Very Easy
Production Ready	✅ Yes	⚠️ Limited	❌ No
#### 🧰 TECH STACK
🔹 Backend
Python
Flask (API server)
🔹 AI / LLM
OpenRouter API
GPT-4o-mini model
Prompt Engineering
🔹 Frameworks
LangChain (in version 2)
🔹 Database
SQLite (db.sqlite3)
SQLDatabase (LangChain utility)
🔹 Communication
REST API (/ask endpoint)
JSON requests/responses
#### ⚙️ HOW IT WORKS (GLOBAL PIPELINE)
User Input (Darija / Arabic / English)
        ↓
Translation (→ English)
        ↓
LLM generates SQL query
        ↓
Query executed on SQLite database
        ↓
Result retrieved
        ↓
LLM generates response (Darija)
#### 🔐 ENVIRONMENT SETUP

Set your API key:

setx OPENROUTER_API_KEY "your_api_key"
#### ▶️ RUN THE PROJECT
pip install flask langchain langchain-openai requests
python app.py

Open:

http://127.0.0.1:5000
