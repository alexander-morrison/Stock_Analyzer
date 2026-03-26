import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input="Say 'OpenAI connection successful.'"
)

alpha_key = os.getenv("ALPHAVANTAGE_API_KEY")

print("Alpha Vantage Key Loaded:", alpha_key)
print(response.output_text)
