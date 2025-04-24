from typing import Dict, Any, List
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from util.tool import tool_tavily, tavily_client, send_email, generate_image, generate_audio

class ToolAgent:
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.tools = {
            'search': tool_tavily,
            'extract': tavily_client.extract,
            'email': send_email,
            'generate_image': self._generate_image,
            'generate_audio': self._generate_audio
        }
        
        self.system_prompt = """You are a tool agent responsible for executing specific tasks using available tools.
        For each task, you should:
        1. Identify the appropriate tool for the task
        2. Execute the task using the selected tool
        3. Return the result and any relevant feedback
        4. Handle errors gracefully and provide meaningful feedback"""
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            ("system", "Execute the given task using the most appropriate tool. Return the result and any feedback.")
        ])

    def execute_task(self, state: Dict[str, Any], task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task using the appropriate tool."""
        # Create a ReAct agent with available tools
        agent = create_react_agent(self.llm, tools=list(self.tools.values()))
        
        # Execute the task
        result = agent.invoke({
            "messages": [HumanMessage(content=task["description"])]
        })
        
        return {
            "result": result["messages"][-1].content,
            "status": "completed",
            "feedback": self._generate_feedback(result["messages"][-1].content)
        }

    def _generate_feedback(self, result: str) -> str:
        """Generate feedback based on the task execution result."""
        feedback_prompt = ChatPromptTemplate.from_messages([
            ("system", "Analyze the task execution result and provide feedback on:\n"
                      "1. Success or failure of the task\n"
                      "2. Quality of the result\n"
                      "3. Potential improvements\n"
                      "4. Any issues encountered"),
            ("system", f"Task result: {result}\nProvide detailed feedback.")
        ])
        
        chain = feedback_prompt | self.llm
        return chain.invoke({})

    def _generate_image(self, prompt: str) -> str:
        """Generate an image using Google's Gemini."""
        result = generate_image(prompt)
        if result:
            return f"Image generated successfully: {result}"
        return "Failed to generate image"

    def _generate_audio(self, text: str, voice: str = "alloy") -> str:
        """Generate audio using Google's Text-to-Speech."""
        result = generate_audio(text, voice)
        if result:
            return f"Audio generated successfully: {result}"
        return "Failed to generate audio" 