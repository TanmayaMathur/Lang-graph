import os
import requests
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from tavily import TavilyClient
import smtplib
from email.mime.text import MIMEText
from util.file_util import FileUtils
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Initialize Tavily tools
tool_tavily = TavilySearchResults(max_results=5)
tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

def send_email(subject: str, body: str, to_email: str) -> None:
    """Send an email using SMTP."""
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('EMAIL_CODE')

    message = MIMEText(body, 'plain')
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def generate_image(prompt: str) -> str:
    """Generate an image using Groq."""
    try:
        # Generate image using Groq
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Generate an image based on this description: {prompt}"}],
            model="llama2-70b-4096",
            temperature=0.7
        )
        
        # Save the image
        file_name = f"{FileUtils.random_uuid()}.png"
        folder = f"uploadFiles/{FileUtils.get_folder()}/"
        file_path = os.path.join(os.getenv('FILE_ROOT_PATH', 'uploads'), folder)
        
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            
        # Save the image data
        with open(os.path.join(file_path, file_name), 'wb') as f:
            f.write(response.choices[0].message.content.encode())
            
        relative_path = os.path.join(folder, file_name)
        return f"{os.getenv('BASE_URL', 'http://localhost:8000')}/{relative_path}"
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def generate_audio(text: str, voice: str = "alloy") -> str:
    """Generate audio using Groq."""
    try:
        # Generate audio using Groq
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Generate audio for this text: {text}"}],
            model="llama2-70b-4096",
            temperature=0.7
        )
        
        # Save the audio
        file_name = f"{FileUtils.random_uuid()}.mp3"
        folder = f"uploadFiles/{FileUtils.get_folder()}/"
        file_path = os.path.join(os.getenv('FILE_ROOT_PATH', 'uploads'), folder)
        
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            
        # Save the audio data
        with open(os.path.join(file_path, file_name), 'wb') as f:
            f.write(response.choices[0].message.content.encode())
            
        relative_path = os.path.join(folder, file_name)
        return f"{os.getenv('BASE_URL', 'http://localhost:8000')}/{relative_path}"
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None 