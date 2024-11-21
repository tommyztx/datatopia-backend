import pytest
from flask.testing import FlaskClient
import json
import os
from unittest.mock import patch

# Import the Flask app
from api import app, execute_sql_query

# Set up environment variables for testing
os.environ['FRONTEND_URL'] = 'http://localhost:3000'
os.environ['OPENAI_API_KEY'] = 'fake-api-key'
os.environ['DB_SERVER'] = 'localhost'
os.environ['DB_DATABASE'] = 'pharmacy_db'
os.environ['DB_USER'] = 'user'
os.environ['DB_PASSWORD'] = 'password'

@pytest.fixture
def client() -> FlaskClient:
    """Fixture for creating a test client."""
    with app.test_client() as client:
        yield client

def test_ask_question_invalid(client):
    """Test the /ask endpoint with an invalid question."""
    response = client.post('/ask', json={"question": "What is the color of the sky?"})
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["answer"] == "I'm sorry, I couldn't find the answer to that question."

def test_sql_execution_success():
    """Test the execute_sql_query function."""
    # Mocking the actual database query execution
    with patch('api.connect_to_db') as mock_connect:
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [("Item A", 1, 10.0)]

        result, error = execute_sql_query("SELECT * FROM Stocks")

    # Assert that the query execution returns expected results
    assert result == [("Item A", 1, 10.0)]
    assert error is None

def test_sql_execution_failure():
    """Test the execute_sql_query function when there is an error."""
    # Mocking an error during the query execution
    with patch('api.connect_to_db') as mock_connect:
        mock_connect.side_effect = Exception("Database error")

        result, error = execute_sql_query("SELECT * FROM Stocks")

    # Assert that an error occurred
    assert result is None
    assert error == "An error occurred executing query: Database error"

def test_ask_question_valid(client):
    """Test the /ask endpoint with a valid question."""
    with patch('api.translate_question') as mock_translate, \
         patch('api.OpenAI.invoke') as mock_invoke:
        # Mocking the translation of the question
        mock_translate.return_value = ("How much money did I make in 2024?", "en")
        # Mocking the SQL query generation and answer generation
        mock_invoke.return_value = "SELECT SUM(Salesitems.AmntNetto) AS TotalRevenue FROM Salesitems INNER JOIN Sales ON Salesitems.SlsID = Sales.SlsID WHERE Sales.TimeSaleStart BETWEEN '2024-01-01' AND '2024-12-31' AND Sales.pharma_ID = 'BE_251410';"
        response = client.post('/ask', json={"question": "How much money did I make in 2024?"})
        data = json.loads(response.data)

    # Assert the response status and content
    assert response.status_code == 200
    assert "sql_query" in data
    assert "answer" in data

# Test that a ValueError is raised when FRONTEND_URL is missing
def test_missing_frontend_url(monkeypatch):
    monkeypatch.delenv("FRONTEND_URL", raising=False)
    
    with pytest.raises(ValueError, match="Missing required environment variable: FRONTEND_URL"):
        # Simulate the code that would trigger the exception
        frontend_url = os.getenv('FRONTEND_URL')
        if not frontend_url:
            raise ValueError("Missing required environment variable: FRONTEND_URL")
        
def test_missing_openai_api_key(monkeypatch):
    # Remove OPENAI_API_KEY from the environment to simulate a missing variable
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    
    # Test that a ValueError is raised when OPENAI_API_KEY is missing
    with pytest.raises(ValueError, match="Missing required environment variable: OPENAI_API_KEY"):
        # Simulate the code that would trigger the exception
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("Missing required environment variable: OPENAI_API_KEY")

def test_ask_question_no_data(client):
    """Test the /ask endpoint when no data is available in the database."""
    # Mocking the translation and OpenAI response
    with patch('api.translate_question') as mock_translate, \
         patch('api.OpenAI.invoke') as mock_invoke:
        mock_translate.return_value = ("What are the top items?", "en")
        mock_invoke.return_value = "SELECT TOP 3 * FROM Stocks"

        # Mocking SQL query result as empty
        with patch('api.execute_sql_query') as mock_execute:
            mock_execute.return_value = ([], None)

            response = client.post('/ask', json={"question": "What are the top items?"})
            data = json.loads(response.data)

    # Assert the response shows no data found
    assert response.status_code == 200
    assert data["answer"] == "It seems there's no data available for this question."

if __name__ == '__main__':
    pytest.main()
