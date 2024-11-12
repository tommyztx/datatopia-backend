from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from flask_cors import CORS
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
import pandas as pd
import os
import sys
import pyodbc

# Initialize the Flask app
app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])
CORS(app, origins=["http://localhost:3000", "https://vercel-frontend-three-mu.vercel.app"])
    

# Load environment variables
# load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("Missing required environment variable: OPENAI_API_KEY")

# Initialize OpenAI language model
llm = OpenAI(temperature=0, verbose=True, openai_api_key=openai_api_key)

# Load the table metadata
with open("app/schema.sql", 'r') as file:
    table_metadata = file.read().replace('\n', '')

# Prompt templates
question_prompt = PromptTemplate.from_template(
    """Given the following question and table fields, return a SQLite query that retrieves data related to the question. Give adequate column names when possible. The user is the owner of a pharmacy, and the data in the database represents data in the pharmacy. If the question is not related to the database, say "I cannot answer questions that are not related to your pharmacy."

Database Schema: {table_metadata}
Question: {question}
SQL Query: """
)

answer_prompt = PromptTemplate.from_template(
    """Given the user question and SQL result, answer the user question in a friendly and human-like manner to a pharmacist managing their pharmacy, avoiding SQL details- not referencing the SQL result. Any financial information relates to a pharmecist's store, you can provide it because the data is resulting from a SQL qeuery run on their database. If SQL result is [] then there is no data found, and say that. When there is no data, dont ask follow-up questions, but you can make suggestions for other questions. 

Question: {question}
SQL Result: {result}
Answer: """
)

# Transform column names for better readability
def transform_column_names(columns):
    return [col.replace('_', ' ').title() for col in columns]

def connect_to_db():
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_DATABASE')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    driver= '{ODBC Driver 18 for SQL Server}'
    
    conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

    return conn
    
# Function to execute SQL query
def execute_sql_query(query):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        result = cursor.fetchall()
        conn.close()
        return result, columns, None
    except Exception as e:
        return None, None, "An error occurred executing query: " + str(e)

# Endpoint to handle questions
@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get("question")

        # Generate SQL query using the question prompt
        question_chain = question_prompt | llm
        sql_query = question_chain.invoke({
            "table_metadata": table_metadata,
            "question": question
        })

        # Check if the question can be answered
        if sql_query.startswith("I cannot answer questions that are not related to your pharmacy"):
            return jsonify({
                "question": question,
                "sql_query": None,
                "columns": None,
                "data": [],
                "answer": "I'm sorry, I couldn't find the answer to that question."
            })

        # Execute SQL query
        sql_result, columns, error = execute_sql_query(sql_query)
        if error is not None:
            return jsonify({
                "question": question,
                "sql_query": sql_query,
                "columns": None,
                "data": [],
                "answer": "There was an error that occured runnning the query",
                "error" : error
            })
        if sql_result is None or not sql_result:
            return jsonify({
                "question": question,
                "sql_query": sql_query,
                "columns": None,
                "data": [],
                "answer": "It seems there's no data available for this question."
            })

        transformed_columns = transform_column_names(columns)
        result_df = pd.DataFrame(sql_result, columns=transformed_columns).to_dict(orient="records")

        # Generate the final response using the answer prompt
        answer_chain = answer_prompt | llm
        final_answer = answer_chain.invoke({
            "question": question,
            "result": sql_result
        })

        return jsonify({
            "question": question,
            "sql_query": sql_query,
            "columns": transformed_columns,
            "data": result_df,
            "answer": final_answer
        })
    except Exception as e:
        return jsonify({
            "error": "An error occurred executing main: " + str(e)
        })

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
