import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

try:
    print(f"Connecting to: {url}")
    supabase = create_client(url, key)
    # Try a simple query
    res = supabase.table("users").select("*").limit(1).execute()
    print("✅ Connection Successful!")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
    