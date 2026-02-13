import os
from dotenv import load_dotenv
from memory.memory_manager import MemoryManager
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

MODEL_NAME = "gemini-2.5-flash"
CONFIDENCE_THRESHOLD = 0.8
MAX_ITERATIONS = 2
TOKEN_LIMIT = 6000
memory_manager = MemoryManager()