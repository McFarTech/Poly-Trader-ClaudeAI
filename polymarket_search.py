#!/usr/bin/env python3
import anthropic
from datetime import datetime
import os

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def extract_text(response):
    """Concatenate the text blocks from a Claude response."""
    return "".join(block.text for block in response.content if block.type == "text")


# Create a completion using web search
try:
    completion = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": """
                Search Polymarket.com and tell me:
                1. What are the current top 10 trending markets on Polymarket.com?
                2. For each market, provide the market name, current YES/NO odds or prices, and resolution date if available.
                3. Focus especially on US election markets, sports markets, and celebrity markets.
                4. Format as a numbered list with clearly stated odds as percentages.
                """
            }
        ],
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
    )

    # Print results
    print(f"POLYMARKET ACTIVE MARKETS ({datetime.now().strftime('%Y-%m-%d')})")
    print("=" * 70)
    print(extract_text(completion))

except Exception as e:
    print(f"Error: {e}")
