import os
import sys
from dotenv import load_dotenv

def load_config():
    """
    Load configuration from environment variables
    """
    # Ensure environment variables are loaded
    load_dotenv()
    
    # Get Supabase configuration
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    # If configuration is missing, use demo values
    if not supabase_url or not supabase_key:
        print("WARNING: Supabase configuration is missing in .env file.")
        print("Using DEMO MODE with limited functionality.")
        print("To use full functionality, create a .env file with SUPABASE_URL and SUPABASE_KEY.")
        print("")
        
        # Demo values for testing - these won't connect to a real Supabase instance
        supabase_url = "https://demo.supabase.co"
        supabase_key = "demo-anon-key"
    
    return {
        'supabase_url': supabase_url,
        'supabase_key': supabase_key
    }