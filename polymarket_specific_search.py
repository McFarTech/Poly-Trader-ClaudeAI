#!/usr/bin/env python3
import anthropic
from datetime import datetime, timedelta
import os

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def extract_text(response):
    """Concatenate the text blocks from a Claude response."""
    return "".join(block.text for block in response.content if block.type == "text")


# Get tomorrow's date
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

# Specific query mentioning the types of markets we're looking for
query = f"""
Search Polymarket.com for active prediction markets ending tomorrow ({tomorrow}).
Specifically, check for markets like:
1. "Bitcoin Up or Down on March 25?"
2. "Ethereum Up or Down on March 25?"
3. Any markets related to temperature records for March 2025
4. Markets about company market capitalizations ending in March 2025

For each market, provide details about how they will be resolved.
"""

# Make the API call with web search enabled
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    system="You are a research assistant with web search capabilities to find current information about Polymarket prediction markets.",
    messages=[
        {"role": "user", "content": query}
    ],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
)

# Print the response
print(f"POLYMARKET MARKETS ENDING TOMORROW ({tomorrow})")
print("=" * 80)
print(extract_text(response))
