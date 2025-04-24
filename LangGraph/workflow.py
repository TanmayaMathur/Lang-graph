from typing import Dict, Any, List, TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import END, START, StateGraph
import operator
from agents.plan_agent import PlanAgent, SubTask
from agents.tool_agent import ToolAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    tasks: List[SubTask]
    current_task_index: int
    feedback: str

def create_workflow():
    # Initialize agents with Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7,
        convert_system_message_to_human=True
    )
    plan_agent = PlanAgent(llm)
    tool_agent = ToolAgent(llm)
    
    # Create workflow graph
    workflow = StateGraph(AgentState)
    
    # Define nodes
    def plan_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate initial plan or update plan based on feedback."""
        if not state.get("tasks"):
            # Initial planning
            tasks = plan_agent.plan(state)
        else:
            # Update plan based on feedback
            tasks = plan_agent.update_plan(state, state.get("feedback", ""))
        
        return {
            "messages": state["messages"],
            "tasks": tasks,
            "current_task_index": 0,
            "feedback": ""
        }
    
    def execute_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the current task."""
        current_task = state["tasks"][state["current_task_index"]]
        result = tool_agent.execute_task(state, current_task.dict())
        
        # Update task with result and feedback
        current_task.result = result["result"]
        current_task.status = result["status"]
        current_task.feedback = result["feedback"]
        
        return {
            "messages": state["messages"] + [HumanMessage(content=result["result"])],
            "tasks": state["tasks"],
            "current_task_index": state["current_task_index"],
            "feedback": result["feedback"]
        }
    
    def should_continue(state: Dict[str, Any]) -> str:
        """Determine if we should continue with the next task or go back to planning."""
        if state["current_task_index"] >= len(state["tasks"]) - 1:
            return "plan" if state["feedback"] else "end"
        return "execute"
    
    # Add nodes to workflow
    workflow.add_node("plan", plan_node)
    workflow.add_node("execute", execute_node)
    
    # Add edges
    workflow.add_edge(START, "plan")
    workflow.add_conditional_edges(
        "execute",
        should_continue,
        {
            "plan": "plan",
            "execute": "execute",
            "end": END
        }
    )
    
    # Compile workflow
    return workflow.compile()

# Example usage
if __name__ == "__main__":
    workflow = create_workflow()
    
    # Run workflow with initial user query
    for state in workflow.stream({
        "messages": [HumanMessage(content="Search for information about Python and send me an email with the results")]
    }):
        if "__end__" not in state:
            print(state)
            print("---") 