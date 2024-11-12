# Pharmacy Data Query Bot

This project is a demo of a **Pharmacy Data Query Bot** built using `LangChain`, `Streamlit`, and `SQLite`. The bot allows users to ask questions about pharmacy sales, customer data, and product information, and provides human-like responses based on SQL queries executed on an SQLite database.

## Features

- Interactive Streamlit UI for asking questions and displaying answers
- Preloaded frequently asked questions (FAQs) in a sidebar for quick access
- Executes SQL queries on customer, order, and product data
- Provides responses in a human-like conversational manner
- FAQ answers, user questions, and responses are stored in session history for easy access

## Requirements

- Python 3.8+
- Required libraries (On virtual environment):
  - `langchain`
  - `streamlit`
  - `dotenv`
  - `sqlite3`

## Installation and Setup

1. **Enter Correct Directory**:

   ```bash
   cd demolang

   ```

2. **Environment Variables**:

   ```bash
   OPENAI_API_KEY="Your Open API Key"

   ```

3. **Run Virtual Environment**:

   ```bash
   source venv/bin/activate

   ```

4. **Install Requirements**:

   ```bash
   pip install requirements.txt

   ```

5. **Run Backend Server**:

   ```bash
   python api.py

   ```

6. **Interact with the bot:**:
   - Enter your own questions in the text box provided.
   - Click on a preloaded FAQ on the sidebar to quickly get answers to common questions.
