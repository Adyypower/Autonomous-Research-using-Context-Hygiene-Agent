from ddgs import DDGS
import json

def search_web(query: str):
    """
    Executes a web search using the direct DDGS library for better reliability.
    """
    try:
        print(f"DEBUG: Searching DDGS for: {query}")
        results = []
        
        # Use the context manager for DDGS
        with DDGS() as ddgs:
            # text() returns an iterator of results
            # max_results=5 to match our previous logic
            ddgs_gen = ddgs.text(query, max_results=5)
            if ddgs_gen:
                for r in ddgs_gen:
                    # r is typically {'title':..., 'href':..., 'body':...}
                    title = r.get('title', 'No Title')
                    link = r.get('href', 'No Link')
                    body = r.get('body', '')
                    
                    results.append(f"Source: {link}\nTitle: {title}\nContent: {body}")

        if not results:
            return f"No results found for '{query}'."

        return "\n\n".join(results)

    except Exception as e:
        return f"Error executing search: {e}"