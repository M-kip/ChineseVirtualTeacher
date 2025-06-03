import os
import sys
from transformers import LlamaTokenizerFast
from google import genai
from google.genai import types
from google.api_core import retry
from dotenv import load_dotenv

# Load environment variables from .env file 
load_dotenv()
# Set up the tokenizer with a maximum length
# This is a simple script to generate responses using the Google Gemini API
pretrained_model = "hf-internal-testing/llama-tokenizer"
maxlength = sys.maxsize
tokenizer = LlamaTokenizerFast.from_pretrained(pretrained_model, legacy=False)
tokenizer.model_max_length = maxlength
max_tokens = 1000

# Truncate chunks in shorter version the the context preserved 
def truncate_string(string, max_tokens):
    # Tokenize the text and count the tokens
    tokens = tokenizer.encode(string, add_special_tokens=True)
    # Truncate the tokens to max len
    truncated_tokens = tokens[:max_tokens]
    # Transform the tokens back to text
    truncated_text = tokenizer.decode(truncated_tokens)
    return truncated_text


def trancute_docs(docs, max_tokens=max_tokens):
    """
    Truncate the documents to fit within the max token limit.
    """
    # Transform docs into a string arrary using the "payload" key
    docs_as_one_string = "\n=========\n".join([doc['text'] for doc in docs])
    docs_truncated = truncate_string(docs_as_one_string, max_tokens=max_tokens)
    
    return docs_truncated


def get_prompt(truncated_docs, query_text):
    prompt = f"""
    <s> [INST] <<SYS>>
    You are a helpful assistant named "Virtual Chinese Teacher Chatbot."

    Your job is to help users learn Chinese using only the knowledge from the HSK 1 textbook.
    - Do NOT reference the source directly.
    - Do NOT say "according to the source."
    - Present answers as if they are your own.
    - Use the same style, tone, and difficulty as HSK 1-3 textbook.
    - Use short and clear examples.
    <</SYS>> [/INST]

    Respond precisely to this question: "{query_text}"

    Use the information below as your main source of knowledge.
    You may also rely on general HSK 1-3 level Chinese teaching principles.
    Make your answer educational, friendly, and easy to understand.

    ====
    SOURCE:
    {truncated_docs}

    Your response should have at most THREE PARAGRAPHS.
    Each paragraph should be no more than 50 words.
    Keep your writing clear, minimal, and focused (Spartan style).

    [/INST]
    """
    return prompt


def init_googleai():
    is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

    # Set up a retry helper. This allows you to "Run all" without worrying about per-minute quota.
    genai.models.Models.generate_content = retry.Retry(
        predicate=is_retriable)(genai.models.Models.generate_content)

    # The Python SDK uses a Client object to make requests to the API. 
    # The client lets you control which back-end to use (between the Gemini API and Vertex AI) and handles authentication (the API key).
    client = genai.Client(api_key=os.getenv('GENAI_API_KEY'))
    chat = client.chats.create(model='gemini-2.0-flash', history=[],)
    return chat

def generate_response(query_text, docs, chat=None):
    if chat is None:
        chat = init_googleai()
    truncated_documents = trancute_docs(docs)
    promt = get_prompt(truncated_documents, query_text)
    response = chat.send_message(promt)
    return response.text