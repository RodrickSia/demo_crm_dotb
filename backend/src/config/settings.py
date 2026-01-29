
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the src directory
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_API_KEY = os.getenv('SUPABASE_API_KEY')
assert SUPABASE_URL is not None, "SUPABASE_URL is not set in environment variables."
assert SUPABASE_API_KEY is not None, "SUPABASE_API_KEY is not set in environment variables."

TABLES = [
    "Calls",
    "Journey",
    "Student",
    "attendance",
    "enrollments",
    "meetings",
    "notes",
    "receipts",
    "tasks"
]
