from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from language import translate_question
import os
import pyodbc

# Load environment variables
load_dotenv()

frontend_url = os.getenv('FRONTEND_URL')
if not frontend_url:
    raise ValueError("Missing required environment variable: FRONTEND_URL")


# Initialize the Flask app
app = Flask(__name__)
CORS(app, origins=[frontend_url])
    
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("Missing required environment variable: OPENAI_API_KEY")

# Initialize OpenAI language model
llm = OpenAI(temperature=0, verbose=True, openai_api_key=openai_api_key)

# Load the table metadata
with open("schema.sql", 'r') as file:
    table_metadata = file.read().replace('\n', '')

# Prompt templates
question_prompt = PromptTemplate.from_template(
    """Given the following question and table fields, return a SQL query for a Microsoft Database that retrieves data related to the question. Give adequate column names when possible. The user is the owner of a pharmacy, and the data in the database represents data in the pharmacy. If the question is not related to the database, say "I cannot answer questions that are not related to your pharmacy". 

    IMPORTANT: Use TOP instead of LIMIT when getting a few items. 
    Incorrect example using limit: 

    SELECT Articles.ArtName, Stocks.ArtID, (PubPricePerUnit - BuyPricePerUnit) AS Margin
            FROM Stocks
            INNER JOIN Articles ON Stocks.ArtID = Articles.ArtID
            WHERE Stocks.pharma_ID = 'BE_251410'
            ORDER BY Margin ASC
            LIMIT 1;

    Correct example using Top: 

    SELECT TOP 1 Articles.ArtName, Stocks.ArtID, (PubPricePerUnit - BuyPricePerUnit) AS Margin
            FROM Stocks
            INNER JOIN Articles ON Stocks.ArtID = Articles.ArtID
            WHERE Stocks.pharma_ID = 'BE_251410'
            ORDER BY Margin ASC
            
    Examples for table relations and formatting:

    Question: How many items do I have with negative margin?
    Answer: SELECT Count(ArtId) FROM Stocks WHERE (PubPricePerUnit - BuyPricePerUnit) < 0 AND pharma_ID = 'BE_251410'

    Question: What is my Top 3 most expensive item? 
    Answer: SELECT TOP 3 Articles.ArtName, Stocks.ArtID, Stocks.PubPricePerUnit
                FROM Stocks
                INNER JOIN Articles ON Stocks.ArtID = Articles.ArtID
                WHERE Stocks.pharma_ID = 'BE_251410'
                ORDER BY Stocks.PubPricePerUnit DESC;

    Question: What are three items that have not sold within the past month?
    Answer: SELECT TOP 3 
            Articles.ArtName,
            Stocks.ArtID,
            Stocks.PubPricePerUnit
        FROM Stocks
        INNER JOIN Articles ON Stocks.ArtID = Articles.ArtID
        LEFT JOIN Salesitems ON Stocks.ArtID = Salesitems.ArtIDSold
        LEFT JOIN Sales ON Salesitems.SlsID = Sales.SlsID
        WHERE Sales.TimeSaleStart IS NULL 
        OR Sales.TimeSaleStart < DATEADD(MONTH, -1, GETDATE())
        ORDER BY Stocks.PubPricePerUnit DESC;

Database Schema: {table_metadata}
Question: {question}
SQL Query: """
)

answer_prompt = PromptTemplate.from_template(
    """Given the user question and SQL result, answer the user question in a friendly and human-like manner to a pharmacist managing their pharmacy, avoiding SQL details- not referencing the SQL result. Any financial information relates to a pharmecist's store, you can provide it because the data is resulting from a SQL qeuery run on their database. If SQL result is [] then there is no data found, and say that. When there is no data, dont ask follow-up questions. 
        All money is in euros!
Question: {question}
SQL Result: {result}
Speak in a {tone} manner.
Generate the answer in {language}
Answer: """
)

def connect_to_db():
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_DATABASE')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    driver= '{ODBC Driver 18 for SQL Server}'
    
    conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password + ';Connection Timeout=300')

    return conn
    
# Function to execute SQL query
def execute_sql_query(query):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result, None
    except Exception as e:
        return None, "An error occurred executing query: " + str(e)

# Endpoint to handle questions
@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get("question")
        tone = data.get("tone", "friendly")
        new_question, language = translate_question(question)

        print("QUESTION", new_question)
        print("LANGUAGE", language)

        # Generate SQL query using the question prompt
        question_chain = question_prompt | llm
        sql_query = question_chain.invoke({
            "table_metadata": table_metadata,
            "question": new_question
        })

        print("SQL Query", sql_query)

        # Check if the question can be answered
        if sql_query.startswith("I cannot answer questions that are not related to your pharmacy"):
            return jsonify({
                "question": question,
                "sql_query": None,
                "answer": "I'm sorry, I couldn't find the answer to that question."
            })

        # Execute SQL query
        sql_result, error = execute_sql_query(sql_query)
        if error is not None:
            return jsonify({
                "question": question,
                "sql_query": sql_query,
                "answer": "There was an error that occured runnning the query",
                "error" : error
            })
        if sql_result is None or not sql_result:
            return jsonify({
                "question": question,
                "sql_query": sql_query,
                "answer": "It seems there's no data available for this question."
            })
        
        # Generate the final response using the answer prompt
        answer_chain = answer_prompt | llm
        final_answer = answer_chain.invoke({
            "question": new_question,
            "result": sql_result,
            "language" : language, 
            "tone": tone
        })

        return jsonify({
            "question": question,
            "sql_query": sql_query,
            "answer": final_answer
        })
    except Exception as e:
        return jsonify({
            "error": "An error occurred executing main: " + str(e)
        })

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
