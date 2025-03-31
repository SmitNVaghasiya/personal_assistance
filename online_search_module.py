from googlesearch import search

def online_search(query, num_results=5):
    try:
        results = list(search(query, num_results=num_results))
        if results:
            response = "Here are the top results:\n"
            for i, url in enumerate(results, 1):
                response += f"Result {i}: {url}\n"
            return response
        return "No results found."
    except Exception as e:
        return f"Error performing online search: {e}"