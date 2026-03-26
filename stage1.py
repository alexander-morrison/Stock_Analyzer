import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

alpha_key = os.getenv("ALPHAVANTAGE_API_KEY")
client = OpenAI()

instructions = """
You are a helpful financial agent using Alpha Vantage MCP tools.
CRITICAL: Use EXACT format for tools:
TOOL_CALL(tool_name="TIME_SERIES_DAILY", arguments={"symbol": "AAPL", "outputsize": "compact"})
List tools first with TOOL_LIST if needed. Available: TIME_SERIES_DAILY, RSI, COMPANY_OVERVIEW.
NEVER use mcp_call or other names.
"""

prompt = """
## Task: AAPL Stock Summary (last 3 days)
1. Retrieve data: TOOL_CALL(tool_name="TIME_SERIES_DAILY", arguments={"symbol": "AAPL", "outputsize": "compact"})
2. Analyze: price movement, day-over-day % change, volume changes.
Output summary only after data.
"""

response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{
        "type": "mcp",
        "server_label": "AlphaVantage",
        "server_url": "https://mcp.alphavantage.co/mcp",
        "authorization": alpha_key,
        "require_approval": "never",
    }],
    input=prompt
)

print(response.output)
print("\n---\n")
print(response.output_text)
