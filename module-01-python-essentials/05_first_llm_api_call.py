# My first ever QnA with an LLM programmatically.
import os
from pathlib import Path
from dotenv import load_dotenv

# 1. New import syntax
from google import genai

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set. Add it to your environment or .env file.")

# 2. New client initialization
client = genai.Client(api_key=api_key)

# 3. New generation method
response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="How far is the moon from earth? Keep it short.",
    # generation_config is now passed via a 'config' parameter
    config={"max_output_tokens": 1024,
            "thinking_config": {"thinking_budget": 0}} 
)

print("\nThe LLM's response:\n")
print(response.text)
print("\n")

# --- What else is in the response? Let us explore: ---
print("Tokens YOU sent\t\t\t:", response.usage_metadata.prompt_token_count)
print("Tokens Gemini replied with\t:", response.usage_metadata.candidates_token_count)
print("Total tokens used\t\t:", response.usage_metadata.total_token_count)
