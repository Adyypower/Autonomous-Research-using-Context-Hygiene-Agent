try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("Import successful!")
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="TEST")
    print("Instantiation successful!")
except Exception as e:
    print(f"Error: {e}")
