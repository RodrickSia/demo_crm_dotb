
from supabase import create_client, Client
from .settings import SUPABASE_URL, SUPABASE_API_KEY

if SUPABASE_URL is None or SUPABASE_API_KEY is None:
    raise ValueError("SUPABASE_URL and SUPABASE_API_KEY must be set in environment variables.")

client: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def get_db_client() -> Client:
    return client
