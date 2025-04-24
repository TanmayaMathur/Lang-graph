from workflow import create_workflow
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if all required environment variables are set."""
    required_vars = ['GROQ_API_KEY', 'TAVILY_API_KEY', 'EMAIL_ADDRESS', 'EMAIL_CODE']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"- {var}")
        print("\nPlease set these variables in your .env file")
        return False
    return True

def run_agent():
    """Run the multi-agent system with user input."""
    # Create the workflow
    workflow = create_workflow()
    
    print("\n=== Multi-Agent System ===")
    print("Type 'exit' to quit")
    print("Example queries:")
    print("1. 'Search for the latest developments in AI and send me an email with the findings'")
    print("2. 'Generate an image of a futuristic city with flying cars'")
    print("3. 'Generate an audio reading of the poem The Road Not Taken'")
    print("\nEnter your query:")
    
    while True:
        # Get user input
        user_query = input("\n> ").strip()
        
        # Check for exit command
        if user_query.lower() == 'exit':
            print("Goodbye!")
            break
        
        # Skip empty queries
        if not user_query:
            continue
        
        print("\nProcessing your query...")
        
        # Run the workflow
        try:
            for state in workflow.stream({
                "messages": [HumanMessage(content=user_query)]
            }):
                if "__end__" not in state:
                    # Print the current state
                    if "messages" in state and state["messages"]:
                        last_message = state["messages"][-1]
                        if hasattr(last_message, 'content'):
                            print(f"\n{last_message.content}")
                    
                    # Print task status if available
                    if "tasks" in state and state["tasks"]:
                        current_task = state["tasks"][state["current_task_index"]]
                        print(f"\nCurrent task: {current_task.description}")
                        print(f"Status: {current_task.status}")
                        if current_task.result:
                            print(f"Result: {current_task.result}")
                        if current_task.feedback:
                            print(f"Feedback: {current_task.feedback}")
                    
                    print("---")
        except Exception as e:
            print(f"\nError: {str(e)}")
        
        print("\nEnter your next query (or 'exit' to quit):")

if __name__ == "__main__":
    if check_environment():
        run_agent() 