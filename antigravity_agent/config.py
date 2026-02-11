import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

MODEL_NAME = "gemini-2.5-flash"
CONFIDENCE_THRESHOLD = 0.7
MAX_ITERATIONS = 3
TOKEN_LIMIT = 6000
