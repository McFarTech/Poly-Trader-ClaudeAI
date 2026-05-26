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

# The exact query from the web interface, with slightly improved wording
query = f"what are the active markets on polymarket.com that are ending tomorrow ({tomorrow})?"

# Make the API call with web search enabled
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    system="You are a research assistant with web search capabilities. Search for and retrieve current information from the internet to answer questions accurately.",
    messages=[
        {"role": "user", "content": query}
    ],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
)

# Print the response
print(f"Query: {query}")
print(f"Tomorrow's date: {tomorrow}")
print("=" * 80)
print(extract_text(response))
