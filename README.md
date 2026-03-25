# LAPTOPASSISTANT – AI Chatbot for Database Querying

## Overview

LaptopAssistant is an intelligent AI-powered chatbot that allows users to query a database using natural language (Moroccan Darija, Arabic, or English).

Instead of writing SQL queries manually, users can simply ask questions like:

- "chhal mn client kayn?"
- "chnohoma les pcs li 3ndkom?"

The system automatically:

- Translates the question
- Generates a SQL query
- Executes it on the database
- Returns a human-like response in Darija

---

## Project Architecture & File Versions

This project includes three different implementations of the same idea, each with a different level of control and abstraction:

- Direct API version (manual control – production ready)
- LangChain version (modular & clean)
- Standalone version (testing & debugging)

---

## Version 1 – app.py (Advanced – Direct API Control)

### Description

This is the most advanced and production-ready version. It directly interacts with the LLM using HTTP requests via OpenRouter, giving full control over:

- Prompt engineering
- Output formatting
- Error handling

### Key Features

- Direct API calls using `requests`
- Custom prompt engineering
- SQL cleaning & sanitization
- Strong error handling (SQL errors, missing tables, etc.)
- Darija response generation with structured rules

### Pipeline
```
Darija Question
   ↓
Translate → English
   ↓
Generate SQL (LLM)
   ↓
Execute SQL (SQLite)
   ↓
Generate Darija Response
```

### Why This Version Matters

- Full control over LLM
- More robust and reliable
- Better suited for production

---

## Version 2 – app.py (LangChain Implementation)

### Description

This version uses LangChain to simplify the pipeline using prompt chaining.

### Key Features

- Uses `ChatOpenAI`
- Uses `PromptTemplate`
- Chain-based architecture (`prompt | llm`)
- Cleaner and more modular code

### Pipeline
```
Darija Question
   ↓
Translation Chain
   ↓
SQL Generation Chain
   ↓
Database Execution
   ↓
Darija Response Chain
```

### Pros & Cons

**Pros**
- Clean structure
- Fast development
- Easy to extend

**Cons**
- Less control over LLM
- Harder debugging
- More hallucination risk

---

## Version 3 – app.py (Standalone Pipeline)

### Description

This version is a script-based pipeline (no Flask API). It is used for testing and understanding how the system works step-by-step.

### Key Features

- Runs in terminal
- Step-by-step pipeline execution
- Debug-friendly
- Uses French for output (variation)

### Pipeline
```
Question
   ↓
Translate → French
   ↓
Generate SQL
   ↓
Execute Query
   ↓
Generate Response
```

### Why This Version Is Useful

- Debugging
- Testing prompts
- Understanding pipeline logic

---

## Comparison of the 3 Versions

| Feature          | Direct API | LangChain | Standalone |
|------------------|------------|-----------|------------|
| Control          | High       | Medium    | High       |
| Simplicity       | Medium     | High      | High       |
| Debugging        | Easy       | Harder    | Very Easy  |
| Production Ready | Yes        | Limited   | No         |

---

## Tech Stack

### Backend
- Python
- Flask (API server)

### AI / LLM
- OpenRouter API
- GPT-4o-mini model
- Prompt Engineering

### Frameworks
- LangChain (in version 2)

### Database
- SQLite (`db.sqlite3`)
- SQLDatabase (LangChain utility)

### Communication
- REST API (`/ask` endpoint)
- JSON requests/responses

---

## How It Works (Global Pipeline)
```
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
```

---

## Environment Setup

Set your API key:
```bash
setx OPENROUTER_API_KEY "your_api_key"
```

---

## Run the Project
```bash
pip install flask langchain langchain-openai requests
python app.py
```

Open: http://127.0.0.1:5000

---

## Important – Prompt Engineering Challenge

### Key Observation

One of the main challenges in this project is reliable SQL generation using LLMs.

During development, multiple backend implementations and prompt variations were tested. However, the model often:

- Generates incorrect SQL queries
- Uses non-existent table names (hallucination)
- Produces invalid SQL syntax
- Returns explanations instead of raw SQL
- Misinterprets the database schema

### Why This Happens

LLMs are not inherently aware of your database structure. Even when provided with the schema, they may:

- Guess table names (e.g., `PCs` instead of `pc`)
- Modify column names
- Add unnecessary formatting (markdown, backticks, etc.)

This makes prompt design critical for system reliability.

### Solution – Strong Prompt Engineering

To mitigate these issues, the SQL generation prompt must be strict and well-defined.

#### Example of Improved Prompt
```
You are a SQL expert.

Database schema:
{schema}

IMPORTANT RULES:
- Use ONLY the tables and columns provided in the schema
- DO NOT invent table names
- DO NOT modify or pluralize names
- Table and column names are case-sensitive
- Return ONLY the SQL query
- No explanations, no markdown, no comments

Write a SQL query to answer:
{question}
```
