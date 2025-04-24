from typing import List, Dict, Any
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class SubTask(BaseModel):
    task_id: str
    description: str
    status: str = "pending"
    result: str = ""
    feedback: str = ""

class PlanAgent:
    def __init__(self, client: Groq):
        self.client = client
        self.system_prompt = """You are a planning agent responsible for breaking down complex tasks into smaller, manageable sub-tasks.
        For each user request, you should:
        1. Analyze the request and identify the main components
        2. Break it down into logical sub-tasks
        3. Ensure sub-tasks are clear, specific, and actionable
        4. Consider dependencies between tasks
        5. Return a list of sub-tasks in order of execution"""

    def plan(self, state: Dict[str, Any]) -> List[SubTask]:
        """Generate a plan by breaking down the user's request into sub-tasks."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": state["messages"][-1].content}
        ]
        
        response = self.client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        
        # Parse the LLM response into SubTask objects
        tasks = []
        for i, task_desc in enumerate(result.split('\n')):
            if task_desc.strip():
                tasks.append(SubTask(
                    task_id=f"task_{i+1}",
                    description=task_desc.strip(),
                    status="pending"
                ))
        return tasks

    def update_plan(self, state: Dict[str, Any], feedback: str) -> List[SubTask]:
        """Update the plan based on feedback from task execution."""
        messages = [
            {"role": "system", "content": """Based on the feedback from task execution, update the plan. Consider:
                1. Which tasks need to be modified
                2. Which tasks need to be added
                3. Which tasks can be removed
                4. The new order of tasks"""},
            {"role": "user", "content": state["messages"][-1].content},
            {"role": "system", "content": f"Current feedback: {feedback}\nUpdate the plan accordingly."}
        ]
        
        response = self.client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        
        # Parse the updated plan into SubTask objects
        tasks = []
        for i, task_desc in enumerate(result.split('\n')):
            if task_desc.strip():
                tasks.append(SubTask(
                    task_id=f"task_{i+1}",
                    description=task_desc.strip(),
                    status="pending"
                ))
        return tasks 