#!/usr/bin/env python3
# NOTE: This script now uses the Anthropic Claude API despite its filename.
import anthropic
from datetime import datetime, timedelta
import os

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def extract_text(response):
    """Concatenate the text blocks from a Claude response."""
    return "".join(block.text for block in response.content if block.type == "text")


# Get tomorrow's date
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%B %d, %Y')  # Format: March 25, 2025

try:
    print("Searching Polymarket via Claude with web search...")
    # A single Messages call with the web_search tool replaces the previous
    # create-assistant / create-thread / poll-run flow.
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=f"You are an expert at finding information about Polymarket prediction markets. Today is {datetime.now().strftime('%B %d, %Y')}. Your task is to search for and provide the most up-to-date information about Polymarket markets that are ending tomorrow ({tomorrow}). Focus especially on markets related to Bitcoin, Ethereum, temperature records, and company market capitalizations.",
        messages=[
            {
                "role": "user",
                "content": "what are the active markets on polymarket that are ending tomorrow?"
            }
        ],
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
    )

    # Print the response
    print(f"\nCLAUDE WEB SEARCH - POLYMARKET MARKETS ENDING TOMORROW ({tomorrow})")
    print("=" * 80)
    print(extract_text(response))

except Exception as e:
    print(f"Error: {e}")
