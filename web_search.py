import requests
from config import SERP_API_KEY

def web_search(query):
    """Perform web search using SerpAPI and return summarized results."""
    url = f"https://serpapi.com/search?q={query}&api_key={SERP_API_KEY}"
    response = requests.get(url).json()

    results = response.get("organic_results", [])
    summary = "\n".join([f"{res['title']}: {res['link']}" for res in results[:3]])

    return summary if summary else "No results found."
