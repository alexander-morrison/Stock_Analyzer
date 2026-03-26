import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

alpha_key = os.getenv("ALPHAVANTAGE_API_KEY")

client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    tools=[
        {
            "type": "mcp",
            "server_label": "AlphaVantage",
            "server_url": "https://mcp.alphavantage.co/mcp",
            "authorization": alpha_key,
            "require_approval": "never",
        },
    ],
    input="Confirm that the Alpha Vantage MCP server is available."
)

print(response.output)
print("\n---\n")
print(response.output_text)
