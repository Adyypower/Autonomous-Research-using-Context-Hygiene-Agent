from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(max_results=3)

def search_web(query:str):
    try:
        results = search.invoke(query)
        # Format results as a string for compatibility with existing nodes
        formatted_results = "\n\n".join([
            f"Source: {res.get('url', 'N/A')}\nContent: {res.get('content', 'N/A')}" 
            for res in results
        ])
        return formatted_results
    except Exception as e:
        return f"Error executing search: {e}"