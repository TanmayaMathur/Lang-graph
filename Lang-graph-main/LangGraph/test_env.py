import os
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

def test_environment():
    # Load environment variables
    load_dotenv()
    
    # Test Groq API
    try:
        print("Testing Groq API...")
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello"}],
            model="llama-3.3-70b-versatile"
        )
        print("✅ Groq API key is working")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print("❌ Groq API key error:", str(e))
        print("Full error details:", e.__class__.__name__)
    
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