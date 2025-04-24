from typing import Dict, Any, List
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from util.tool import tool_tavily, tavily_client, send_email, generate_image, generate_audio

class ToolAgent:
    def __init__(self, client: Groq):
        self.client = client
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

    def execute_task(self, state: Dict[str, Any], task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task using the appropriate tool."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": task["description"]}
        ]
        
        response = self.client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        
        # Execute the appropriate tool based on the task
        tool_name = self._identify_tool(result)
        if tool_name in self.tools:
            tool_result = self.tools[tool_name](task["description"])
            feedback = self._generate_feedback(tool_result)
            return {
                "result": tool_result,
                "status": "completed",
                "feedback": feedback
            }
        else:
            return {
                "result": "No appropriate tool found for this task",
                "status": "failed",
                "feedback": "Please try rephrasing the task"
            }

    def _generate_feedback(self, result: str) -> str:
        """Generate feedback based on the task execution result."""
        messages = [
            {"role": "system", "content": """Analyze the task execution result and provide feedback on:
                1. Success or failure of the task
                2. Quality of the result
                3. Potential improvements
                4. Any issues encountered"""},
            {"role": "user", "content": f"Task result: {result}"}
        ]
        
        response = self.client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        
        return response.choices[0].message.content

    def _identify_tool(self, task_description: str) -> str:
        """Identify which tool to use based on the task description."""
        messages = [
            {"role": "system", "content": "Based on the task description, identify which tool to use from: search, extract, email, generate_image, generate_audio"},
            {"role": "user", "content": task_description}
        ]
        
        response = self.client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip().lower()

    def _generate_image(self, prompt: str) -> str:
        """Generate an image using Groq."""
        result = generate_image(prompt)
        if result:
            return f"Image generated successfully: {result}"
        return "Failed to generate image"

    def _generate_audio(self, text: str, voice: str = "alloy") -> str:
        """Generate audio using Groq."""
        result = generate_audio(text, voice)
        if result:
            return f"Audio generated successfully: {result}"
        return "Failed to generate audio" 