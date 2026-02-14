try:
    from duckduckgo_search import DDGS
    print("Imported DDGS from duckduckgo_search")
except ImportError:
    print("Could not import from duckduckgo_search")

try:
    from ddgs import DDGS
    print("Imported DDGS from ddgs")
except ImportError:
    print("Could not import DDGS from ddgs")

try:
    import ddgs
    print(f"Imported ddgs module. Dir: {dir(ddgs)}")
except ImportError:
    print("Could not import ddgs module")
