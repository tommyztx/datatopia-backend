# Pharmacy Data Query Bot

This project is a demo of a **Pharmacy Data Query Bot** built using `LangChain`, `OpenAI`, and `Microsoft SQL`. The bot allows users to ask questions about pharmacy sales, customer data, and product information, and provides human-like responses based on SQL queries executed on an Microsoft Azure database.

**Texas A&M Fall 2024 Capstone Project**

**Sponsor**: Datatopia 

**Instructors**: Professor Pauline Wade, Saba Mostofi

**Students**: Amber Cheng, Gemma Goddard, Thomas Zheng, Justin Ma, Si Holmes

## Features

- Interactive Next.js frontend for asking questions and displaying answers
- Preloaded frequently asked questions (FAQs) in a sidebar for quick access
- Executes SQL queries on a Microsoft SQL database
- Provides responses in a human-like conversational manner
- FAQ answers, user questions, and responses are stored in session history for easy access

## Overview Architecture/Technology Stack

- **Backend:** Flask (python)
- **Database:** Microsoft SQL Server
- **Querying:** LangChain and OpenAI
- **Frontend:** Next.js

## Backend

### Overview

The backend of the chatbot is built using a Flask Python API, which processes incoming questions from the frontend. When a user asks a question, such as "What are the sales for last month?", the Flask app first uses Natural Language Processing (NLP) techniques to interpret the question and extract key details. Based on this interpretation, the app generates an appropriate SQL query, such as querying the sales data for the previous month. The generated SQL query is then executed on the database (e.g., using SQLAlchemy or another database connector), and the results are retrieved. Finally, the backend returns the results to the frontend in JSON format, where they are displayed to the user, allowing the chatbot to provide the requested data. This process enables the chatbot to convert natural language queries into meaningful database queries, providing users with dynamic, data-driven answers.

### Dependencies

- Python 3.8+
- Required libraries (On virtual environment):
  - `python-dotenv==1.0.1`
  - `Flask==3.0.3`
  - `flask_cors==5.0.0`
  - `langchain_core==0.3.12`
  - `langchain_openai==0.2.3`
  - `pyodbc==5.2.0`
  - `gunicorn`
  - `pytest==7.4.0`

## Installation and Setup

1. **Enter Backend Directory**:

   ```bash
   cd backend

   ```

2. **Set Up Environment Variables**:

   ```bash
    OPENAI_API_KEY="your-openai-api-key"
    FRONTEND_URL="your-frontend-url"
    DB_SERVER="your-database-server"
    DB_DATABASE="database-name"
    DB_USER="database-username"
    DB_PASSWORD="database-password"

   ```

3. **Create/Run Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate

   ```

4. **Install Requirements**:

   ```bash
   pip install requirements.txt

   ```
   
5. **Enter App Directory**:

   ```bash
   cd app

   ```

6. **Run Backend Server**:

   ```bash
   python api.py

   ```

You should now be able to send post requests to the API at the ```http://localhost:5000/ask``` route.

**POST request example**:

   ```bash
   {
  "question": "What are 2 items that has not sold within the past 6 month?",
  "tone": "friendly"
}
   ```
   
 ### How to run tests: 
 
In ```app``` , run: 

   ```bash
   pytest test_api.py

   ```


## Frontend

### Overview

This frontend is built with Next.js and Material-UI (MUI) to deliver a responsive, modern user interface. By leveraging Material-UI's rich set of pre-built components and customizable design system, the application ensures a consistent, visually appealing experience. It makes seamless requests to the Flask backend, enabling dynamic interactions and real-time data retrieval. This setup promotes a smooth user experience with clean, scalable, and maintainable code.


### Dependencies 

- ```Node.js (>= 14.x)```
- ```npm (or yarn) for package management```
- ```Next.js```
- ```Material-UI (MUI)```
- ```Axios``` 


## Installation and Setup

1. **Enter Frontend Directory**:

   ```bash
   cd frontend

   ```

2. **Set Up Environment Variables**:

   ```bash
    NEXT_PUBLIC_SERVER_URL="your-backend-url"

   ```
3. **Install dependencies**:

   ```bash
   npm install

   ```

2. **Execute Code**:

   ```bash
    npm run test 

   ```

The development code should be running on ```http://localhost:3000```


## Conclusion

This project represents Phase 1 of the Datatopia initiative. It lays the foundation for a robust data analytics platform designed to evolve in future phases. The next stages aim to integrate advanced capabilities using LangGraph, enabling more complex analyses, predictive insights, and actionable recommendations. This scalable approach ensures that Datatopia continues to deliver deeper and more valuable insights to its users.