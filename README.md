LaptopAssistant – AI Chatbot for Laptop & Client Data

LaptopAssistant is an intelligent chatbot powered by LLMs that allows users to query a database using natural language (Moroccan Darija, Arabic, or English).

The system automatically:

Translates user input
Converts it into SQL queries
Retrieves data from a database
Generates a natural response in Moroccan Darija

👉 The goal is to make data querying accessible to non-technical users through conversational AI.

🧠 Core Features
🌍 Multilingual Support
Accepts Moroccan Darija / Arabic
Translates internally to English for processing
🧾 Natural Language → SQL
Automatically generates SQL queries from user questions
🗄️ Database Integration
Uses SQLite database (db.sqlite3)
Dynamically reads schema
🤖 AI-Powered Responses
Uses LLM via OpenRouter API
Generates human-like answers in Darija
⚡ Real-time API
Built with Flask
REST endpoint for chat interaction
⚙️ How It Works (Pipeline)
User Question (Darija)
        ↓
Translation → English
        ↓
LLM generates SQL query
        ↓
SQL executed on database
        ↓
Result retrieved
        ↓
LLM generates response in Darija
🧰 Tech Stack
Backend: Flask
LLM: OpenRouter (GPT-4o-mini)
Framework: LangChain
Database: SQLite
Language Processing: Prompt Engineering
