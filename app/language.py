from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
import os

# Load environment variables
load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("Missing required environment variable: OPENAI_API_KEY")

# Initialize OpenAI language model
llm = OpenAI(temperature=0, verbose=True, openai_api_key=openai_api_key)

# Prompt template to handle translation
translate_prompt = PromptTemplate.from_template(
    """Translate the following question to English. If in english, return the original question.
    Question: {question}
    Translated Question: 
    """
)

detect_prompt = PromptTemplate.from_template(
    """Return the language that this question is.
    Question: {question}
    Language: 
    """
)
def translate_question(question):
    try:
        # Generate translated question using the translate prompt
        translate_chain = translate_prompt | llm
        translated_response = translate_chain.invoke({
            "question": question
        })

        detect_chain = detect_prompt | llm
        detect_response = detect_chain.invoke({
            "question": question
        })

        return translated_response.strip(), detect_response.strip()

        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None
    
translate_question("Quelles sont mes ventes totales?")