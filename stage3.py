import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

alpha_key = os.getenv("ALPHAVANTAGE_API_KEY")
client = OpenAI()

instructions = """
You are a financial data analyst.
First, call the Alpha Vantage MCP tool to get monthly AAPL data.
Then, you MUST use the python code interpreter tool to write and run Python code
to analyze the data (percentage changes, SMA, volatility, momentum).
Do all calculations with Python code, not in your head, and then explain results
in simple language for a non-technical investor.
"""

prompt = """
## Task
Retrieve monthly stock data for 'AAPL' (last 3 months), then analyze with code_interpreter.

## Steps
1. **Retrieve**: TOOL_CALL(tool_name="TIME_SERIES_MONTHLY", arguments={"symbol": "AAPL", "outputsize": "compact"})

2. **Analyze** (Python code_interpreter) — Calculate:
   - Price trend (% change month-over-month)
   - 3-month SMA and price position relative to it
   - Volatility (standard deviation of monthly returns)
   - Simple momentum score (positive/negative trend direction)

3. **Output** for non-technical investor:
   - Summary: trend direction + strength
   - Risk level (Low/Moderate/High) based on volatility
   - 2-3 plain-language recommendations

## Constraint
No jargon — explain findings simply.
"""

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
        {
            "type": "code_interpreter",
            "container": {
                "type": "auto",
                "memory_limit": "4g"
            }
        }
    ],
    input=prompt
)

print(response.output)
print("\n---\n")
print(response.output_text)
