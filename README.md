# LangGraph Multi-Agent System

A powerful multi-agent system built with LangGraph that enables collaborative task execution through specialized AI agents. The system uses Groq's LLM API for natural language processing and task planning.

## 🌟 Features

- **Multi-Agent Collaboration**: Different agents work together to complete complex tasks
- **Task Planning**: Intelligent breakdown of tasks into manageable sub-tasks
- **Context Management**: Maintains context across different tasks and agents
- **Error Handling**: Graceful error recovery and logging
- **Flexible Architecture**: Easy to extend with new agents and capabilities

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Groq API key
- Tavily API key (for search capabilities)
- Email configuration (for email functionality)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Lang-graph-main.git
cd Lang-graph-main
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API keys:
```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
EMAIL_ADDRESS=your_email
EMAIL_CODE=your_email_app_password
```

## 📁 Project Structure

```
LangGraph/
├── agents/
│   ├── plan_agent.py      # Agent for task planning and breakdown
│   └── tool_agent.py      # Agent for executing specific tools
├── util/
│   └── tool.py           # Utility functions and tool implementations
├── workflow.py           # Main workflow implementation
└── test_env.py          # Environment testing script
```

## 🎯 Usage

### Testing Environment

Before running the main workflow, test your environment setup:

```bash
python LangGraph/test_env.py
```

### Running the Workflow

Run the workflow with a specific task:

```bash
python LangGraph/workflow.py "Your task description here"
```

Example tasks:
1. "Plan a weekend trip to the mountains"
2. "Research and summarize the top 5 AI frameworks"
3. "Create a report about climate change"
4. "Build a basic to-do list web app"
5. "Brainstorm a new product idea"

## 🤖 Agents

The system includes several specialized agents:

1. **Plan Agent**: Breaks down complex tasks into manageable sub-tasks
2. **Tool Agent**: Executes specific tools and actions
3. **Research Agent**: Gathers and analyzes information
4. **Writing Agent**: Creates content and documentation
5. **Review Agent**: Proofreads and provides feedback

## 🛠️ Tools

Available tools include:
- Web search (via Tavily)
- Email sending
- Image generation
- Audio generation
- File operations

## 🔧 Configuration

The system can be configured through:
- Environment variables
- Agent parameters
- Tool settings

## 📝 Example Output

The system provides structured output in the following format:

```
🤖 Processing your request...

📋 Plan Generated:

[Task Breakdown]
- Main Components
- Sub-tasks with assigned agents
- Dependencies and execution order
