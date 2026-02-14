import sys
import os

print("DEBUG: importing search_tool...")

try:
    # Ensure import works
    sys.path.append(os.getcwd())
    from antigravity_agent.tools.search_tool import search_web

    query = "What is the capital of France?"
    print(f"DEBUG: Searching for: {query}")
    result = search_web(query)
    
    print(f"DEBUG: Search Result Sample: {str(result)[:200]}")
    
    if len(result) > 50:
        print("SUCCESS: Search tool works.")
        sys.exit(0)
    else:
        print("FAIL: Search tool returned empty or too short results.")
        sys.exit(1)

except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
