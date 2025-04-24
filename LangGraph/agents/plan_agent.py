from typing import List, Dict, Any
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class SubTask(BaseModel):
    task_id: str
    description: str
    status: str = "pending"
    result: str = ""
    feedback: str = ""

class PlanAgent:
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.system_prompt = """You are a planning agent responsible for breaking down complex tasks into smaller, manageable sub-tasks.
        For each user request, you should:
        1. Analyze the request and identify the main components
        2. Break it down into logical sub-tasks
        3. Ensure sub-tasks are clear, specific, and actionable
        4. Consider dependencies between tasks
        5. Return a list of sub-tasks in order of execution"""
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            ("system", "Based on the user's request, break it down into sub-tasks. Return a list of tasks in order of execution.")
        ])

    def plan(self, state: Dict[str, Any]) -> List[SubTask]:
        """Generate a plan by breaking down the user's request into sub-tasks."""
        chain = self.prompt | self.llm
        result = chain.invoke(state)
        
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
        feedback_prompt = ChatPromptTemplate.from_messages([
            ("system", "Based on the feedback from task execution, update the plan. Consider:\n"
                      "1. Which tasks need to be modified\n"
                      "2. Which tasks need to be added\n"
                      "3. Which tasks can be removed\n"
                      "4. The new order of tasks"),
            MessagesPlaceholder(variable_name="messages"),
            ("system", f"Current feedback: {feedback}\nUpdate the plan accordingly.")
        ])
        
        chain = feedback_prompt | self.llm
        result = chain.invoke(state)
        
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