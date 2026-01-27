from supabase import create_client, Client
from .settings import SUPABASE_URL, SUPABASE_API_KEY

client: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def get_db_client() -> Client:
    return client
