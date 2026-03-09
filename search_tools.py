import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_tool(query: str) -> str:

    try:
        results = client.search(query, max_results=2)

        text = ""
        for r in results["results"]:
            text += r["content"] + "\n"

        return text

    except Exception as e:
        print("Search error:", e)

        # fallback text
        return "General knowledge about the topic without external search."