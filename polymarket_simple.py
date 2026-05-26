#!/usr/bin/env python3
import anthropic
from datetime import datetime
import os

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def extract_text(response):
    """Concatenate the text blocks from a Claude response."""
    return "".join(block.text for block in response.content if block.type == "text")


# Get profitable markets ending soon with betting recommendations
result = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[{"role": "user", "content": """Visit Polymarket.com and analyze:
    1. Find the top 10 most potentially profitable markets that are ending within the next 24 hours
    2. For each market, list: market name, current odds, ending time, and your recommendation on which outcome to bet on
    3. Recommend how much to bet on each market in USD (assume a $1000 total budget)
    4. Calculate expected profit for each bet and total expected profit
    5. Focus on markets with clear mispricing or high potential returns
    """}],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
)

# Print results
print(f"POLYMARKET PROFIT OPPORTUNITIES ({datetime.now().strftime('%Y-%m-%d')})")
print("=" * 70)
print(extract_text(result))
