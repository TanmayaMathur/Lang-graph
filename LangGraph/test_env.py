import os
from dotenv import load_dotenv
import google.generativeai as genai
from tavily import TavilyClient

def test_environment():
    # Load environment variables
    load_dotenv()
    
    # Test Google API
    try:
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello")
        print("✅ Google API key is working")
    except Exception as e:
        print("❌ Google API key error:", str(e))
    
    # Test Tavily
    try:
        tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
        response = tavily_client.search("test query")
        print("✅ Tavily API key is working")
    except Exception as e:
        print("❌ Tavily API key error:", str(e))
    
    # Test Email
    email_code = os.getenv('EMAIL_CODE')
    if email_code and len(email_code.replace(" ", "")) == 16:
        print("✅ Email configuration looks correct")
    else:
        print("❌ Email configuration error: Make sure you have a valid 16-character app password")

if __name__ == "__main__":
    test_environment() 