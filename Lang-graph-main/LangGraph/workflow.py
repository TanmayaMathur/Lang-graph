from typing import Dict, Any, List, TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import END, START, StateGraph
import operator
from agents.plan_agent import PlanAgent, SubTask
from agents.tool_agent import ToolAgent
from groq import Groq
from langchain_core.messages import HumanMessage
import os
import sys

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    tasks: List[SubTask]
    current_task_index: int
    feedback: str

def create_workflow():
    # Initialize agents with Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    plan_agent = PlanAgent(client)
    tool_agent = ToolAgent(client)
    
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
    
    import sys
    user_query = sys.argv[1] if len(sys.argv) > 1 else "Hello, how can I help you?"
    
    print("\n🤖 Processing your request...\n")
    
    # Run workflow with initial user query
    for state in workflow.stream({
        "messages": [HumanMessage(content=user_query)]
    }):
        if "__end__" not in state:
            # Format the output in a more readable way
            if "tasks" in state["plan"]:
                print("📋 Plan Generated:\n")
                for task in state["plan"]["tasks"]:
                    if task.description.startswith("**"):
                        print(f"\n{task.description.strip('*')}")
                    else:
                        print(f"- {task.description}")
                    if task.result:
                        print(f"  Result: {task.result}")
                    if task.feedback:
                        print(f"  Feedback: {task.feedback}")
                print("\n---") 