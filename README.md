# 🚀 Lovable Clone: AI-Powered Application Generator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.6.3-green.svg)](https://github.com/langchain-ai/langgraph)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange.svg)](https://groq.com/)
[![UV Package Manager](https://img.shields.io/badge/UV-Package%20Manager-purple.svg)](https://github.com/astral-sh/uv)

> **A comprehensive agentic application that transforms natural language prompts into fully functional web applications using LangGraph, Groq LLM, and modern Python tooling.**

## 📋 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [⚡ Quick Start Guide](#-quick-start-guide)
- [🏗️ Architecture Overview](#️-architecture-overview)
- [📁 File Structure & Analysis](#-file-structure--analysis)
- [🤖 Core Functions Documentation](#-core-functions-documentation)
- [🔧 Dependencies & Setup](#-dependencies--setup)
- [💡 Usage Examples](#-usage-examples)
- [🔍 API Reference](#-api-reference)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing Guidelines](#-contributing-guidelines)
- [📖 Learning Insights](#-learning-insights)

## 🎯 Project Overview

The Lovable Clone is an **agentic AI application** that demonstrates how modern AI platforms like Lovable.dev might be architected. It showcases the power of multi-agent systems in transforming simple user prompts into complete, functional web applications.

### Key Features

- **🧠 Multi-Agent Architecture**: Three specialized agents (Planner, Architect, Coder) work in sequence
- **📝 Natural Language Processing**: Converts plain English descriptions into technical specifications
- **🔄 Structured Output**: Uses Pydantic schemas for reliable, structured AI responses
- **🛠️ Tool Integration**: Agents have access to file system tools for code generation
- **⚡ Modern Tech Stack**: Built with UV package manager, LangGraph, and Groq LLM

### What Makes This Special

This project provides insights into:
- How agentic applications are structured and built
- The complexity and engineering required for AI-powered code generation
- Practical implementation of LangGraph for multi-step workflows
- Best practices for structured LLM outputs in production systems

## ⚡ Quick Start Guide

### Prerequisites

- Python 3.10 or higher
- [UV package manager](https://github.com/astral-sh/uv) (recommended) or pip
- Groq API key (free at [groq.com](https://groq.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lovable-clone
   ```

2. **Install dependencies using UV** (recommended)
   ```bash
   # Initialize UV project (if not already done)
   uv init
   
   # Install all dependencies
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

4. **Run the application**
   ```bash
   # Using UV
   uv run main.py
   
   # Or using Python directly
   python main.py
   ```

### First Run Example

```bash
$ uv run main.py
Enter your project prompt: Create a colorful modern calculator app in HTML, CSS, and JavaScript

# The system will process your request through three agents:
# 1. Planner: Creates project structure and features
# 2. Architect: Breaks down into implementation tasks  
# 3. Coder: Generates actual code files

# Output files will be created in: agent/generated_project/
```

## 🏗️ Architecture Overview

The application follows a **sequential multi-agent architecture** powered by LangGraph:

### Agent Responsibilities

| Agent | Purpose | Input | Output |
|-------|---------|-------|--------|
| **Planner** | High-level project planning | User prompt | Project plan with files and features |
| **Architect** | Detailed task breakdown | Project plan | Implementation tasks with dependencies |
| **Coder** | Code generation and file creation | Implementation tasks | Actual code files |

### State Management

The application uses a **shared state dictionary** that flows between agents:

```python
State Flow:
{
    "user_prompt": str,           # Initial user input
    "plan": Plan,                 # From Planner
    "task_plan": TaskPlan,        # From Architect  
    "coder_state": CoderState,    # Coder execution state
    "status": str                 # Current execution status
}
```

## 📁 File Structure & Analysis

```
lovable-clone/
├── main.py                    # Entry point and CLI interface
├── pyproject.toml            # Project configuration and dependencies
├── uv.lock                   # Dependency lock file
├── .env                      # Environment variables (create this)
├── agent/                    # Core agent implementation
│   ├── graph.py             # LangGraph workflow and agent definitions
│   ├── prompts.py           # AI prompts for each agent
│   ├── states.py            # Pydantic schemas for structured output
│   ├── tools.py             # File system tools for the coder agent
│   └── generated_project/   # Output directory for generated apps
│       ├── index.html       # Generated HTML files
│       ├── styles.css       # Generated CSS files
│       └── script.js        # Generated JavaScript files (if any)
└── README.md                # This comprehensive documentation
```

### Detailed File Analysis

#### `main.py` - Application Entry Point
**Purpose**: CLI interface and application orchestration  
**Key Components**:
- Argument parsing for recursion limits
- User input handling with graceful error management
- Integration with the LangGraph agent workflow

```python
# Core functionality
def main():
    parser = argparse.ArgumentParser(description="Run engineering project planner")
    parser.add_argument("--recursion-limit", "-r", type=int, default=100)
    
    user_prompt = input("Enter your project prompt: ")
    result = agent.invoke(
        {"user_prompt": user_prompt},
        {"recursion_limit": args.recursion_limit}
    )
```

#### `agent/graph.py` - LangGraph Workflow Engine
**Purpose**: Defines the multi-agent workflow and state management  
**Key Components**:
- Agent function definitions
- LangGraph state graph construction
- Conditional edge logic for iterative coder execution

#### `agent/states.py` - Data Models and Schemas
**Purpose**: Pydantic models for structured AI outputs  
**Key Models**:

```python
class Plan(BaseModel):
    name: str                    # Application name
    description: str             # One-line description
    techstack: str              # Technology stack
    features: list[str]         # Feature list
    files: list[File]           # Required files

class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask]
    model_config = ConfigDict(extra="allow")  # Allows dynamic fields

class CoderState(BaseModel):
    task_plan: TaskPlan
    current_step_idx: int       # Tracks progress
    current_file_content: Optional[str]
```

#### `agent/prompts.py` - AI Prompt Engineering
**Purpose**: Carefully crafted prompts for each agent  
**Design Principles**:
- Clear role definition for each agent
- Specific output format requirements
- Context preservation between agents

#### `agent/tools.py` - File System Interface
**Purpose**: Safe file operations within the generated project directory  
**Security Features**:
- Path validation to prevent directory traversal
- Automatic project directory creation
- UTF-8 encoding for all file operations

## 🤖 Core Functions Documentation

### `coder_agent` Function - Complete Line-by-Line Analysis

The `coder_agent` function is the most complex component of the system. Here's a detailed breakdown:

```python
def coder_agent(state: dict) -> dict:
    """
    LangGraph tool-using coder agent that executes implementation tasks.
    
    This function represents the core of the code generation system,
    iteratively processing implementation tasks and generating code files.
    
    Args:
        state (dict): LangGraph state containing:
            - task_plan: TaskPlan with implementation steps
            - coder_state: Current execution state (optional)
            
    Returns:
        dict: Updated state with coder_state and status
    """
```

#### Line-by-Line Breakdown

**Lines 42-44: State Initialization**
```python
coder_state: CoderState = state.get("coder_state")
if coder_state is None:
    coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)
```
- **Purpose**: Initialize or retrieve the coder's execution state
- **Logic**: On first run, create new CoderState; on subsequent runs, use existing state
- **Why Important**: Enables stateful iteration through multiple implementation tasks

**Lines 46-48: Completion Check**
```python
steps = coder_state.task_plan.implementation_steps
if coder_state.current_step_idx >= len(steps):
    return {"coder_state": coder_state, "status": "DONE"}
```
- **Purpose**: Check if all implementation tasks are completed
- **Logic**: Compare current step index with total number of steps
- **Flow Control**: Triggers graph termination when all tasks are done

**Lines 50: Current Task Selection**
```python
current_task = steps[coder_state.current_step_idx]
```
- **Purpose**: Get the current task to be executed
- **Data Access**: Extracts ImplementationTask object containing filepath and description

**Lines 52-57: File Reading with Error Handling**
```python
try:
    existing_content = read_file.invoke({"path": current_task.filepath})
except Exception as e:
    print(f"Error reading file {current_task.filepath}: {e}")
    existing_content = ""
```
- **Purpose**: Attempt to read existing file content for modification
- **Error Handling**: Gracefully handle non-existent files by setting empty content
- **Tool Usage**: Uses LangChain tool invocation pattern

**Lines 59-65: Prompt Construction**
```python
system_prompt = coder_system_prompt()
user_prompt = (
    f"Task: {current_task.task_description}\n"
    f"File: {current_task.filepath}\n"
    f"Existing content:\n{existing_content}\n"
    "Use write_file(path, content) to save your changes."
)
```
- **Purpose**: Create detailed prompts for the LLM
- **Context Provision**: Includes task description, target file, and existing content
- **Tool Instruction**: Explicitly tells the LLM how to save changes

**Lines 67-68: Tool Setup and Agent Creation**
```python
coder_tools = [read_file, write_file, list_files, get_current_directory]
react_agent = create_react_agent(llm, coder_tools)
```
- **Purpose**: Prepare the ReAct (Reasoning + Acting) agent with file system tools
- **Tool Access**: Provides LLM with ability to interact with the file system
- **Agent Pattern**: Uses LangChain's ReAct pattern for tool-using agents

**Lines 70-81: Agent Execution with Error Handling**
```python
try:
    result = react_agent.invoke({"messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]})
    
    coder_state.current_step_idx += 1
    return {"coder_state": coder_state, "status": "STEP_COMPLETED", "result": result}
    
except Exception as e:
    print(f"Error executing coder agent for step {coder_state.current_step_idx}: {e}")
    return {"coder_state": coder_state, "status": "ERROR", "error": str(e)}
```
- **Purpose**: Execute the ReAct agent and handle results
- **Success Path**: Increment step counter and return completion status
- **Error Path**: Capture and return error information without crashing
- **State Management**: Ensures state is always returned for graph continuation

### Supporting Functions

#### `planner_agent(state: dict) -> dict`
```python
def planner_agent(state: dict) -> dict:
    user_prompt = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
    return {"plan": resp}
```
- **Purpose**: Convert user prompt into structured project plan
- **Structured Output**: Uses Pydantic schema to ensure consistent format
- **Single Responsibility**: Focuses only on high-level planning

#### `architect_agent(state: dict) -> dict`
```python
def architect_agent(state: dict) -> dict:
    plan = state["plan"]
    resp = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan))
    if resp is None:
        raise ValueError("No task plan found")
    resp.plan = plan  # Preserve context
    return {"task_plan": resp}
```
- **Purpose**: Break down plan into detailed implementation tasks
- **Context Preservation**: Adds original plan to response for downstream use
- **Error Handling**: Validates that a task plan was generated

### Graph Construction and Flow Control

```python
graph = StateGraph(dict)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)
```
- **Sequential Flow**: Planner → Architect → Coder
- **Iterative Coder**: Coder loops until all tasks are completed
- **Conditional Termination**: Graph ends when coder status is "DONE"

## 🔧 Dependencies & Setup

### Why UV Package Manager?

This project uses [UV](https://github.com/astral-sh/uv) as the Python package manager for several key advantages:

- **⚡ Speed**: 10-100x faster than pip for dependency resolution
- **🔒 Reliability**: Produces consistent, reproducible builds
- **🎯 Modern**: Built with Rust, designed for modern Python workflows
- **📦 Simplicity**: Single command for project setup and dependency management

### Dependency Analysis

```toml
[project]
dependencies = [
    "groq>=0.31.0",           # Groq LLM API client
    "langchain>=0.3.27",      # LLM framework and utilities
    "langchain-core>=0.3.72", # Core LangChain components
    "langchain-groq>=0.3.7",  # Groq integration for LangChain
    "langgraph>=0.6.3",       # Graph-based agent workflows
    "pip>=25.2",              # Python package installer
    "pydantic>=2.11.7",       # Data validation and serialization
    "python-dotenv>=1.1.1",   # Environment variable management
]
```

#### Key Dependencies Explained

| Package | Purpose | Why This Version |
|---------|---------|------------------|
| **groq** | LLM API access | Latest stable for optimal performance |
| **langchain** | LLM orchestration framework | Core functionality for agent creation |
| **langgraph** | Multi-agent workflows | Graph-based agent coordination |
| **pydantic** | Data validation | Structured output from LLMs |
| **python-dotenv** | Environment management | Secure API key handling |

### Environment Setup

Create a `.env` file in the project root:

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional debugging
LANGCHAIN_DEBUG=true
LANGCHAIN_VERBOSE=true
```

## 💡 Usage Examples

### Basic Usage

```bash
$ uv run main.py
Enter your project prompt: Create a simple todo app with dark mode
```

### Advanced Usage with Custom Recursion Limit

```bash
$ uv run main.py --recursion-limit 50
Enter your project prompt: Build a complex dashboard with multiple charts
```

### Programmatic Usage

```python
from agent.graph import agent

# Direct agent invocation
result = agent.invoke(
    {"user_prompt": "Create a portfolio website"},
    {"recursion_limit": 100}
)

print("Generated files:", result.get("coder_state", {}).get("task_plan", {}).get("implementation_steps", []))
```

### Example Prompts and Expected Outputs

#### Simple Calculator App
**Input**: `"Create a simple calculator web application"`

**Expected Output Structure**:
- `index.html` - Main HTML structure
- `styles.css` - Calculator styling
- `script.js` - Calculator logic and event handling

#### Todo Application
**Input**: `"Build a todo app with add, delete, and mark complete features"`

**Expected Output Structure**:
- `index.html` - Todo interface
- `styles.css` - Modern styling with themes
- `script.js` - Todo management logic
- Local storage integration

## 🔍 API Reference

### Core Classes

#### `Plan`
```python
class Plan(BaseModel):
    name: str                    # Application name
    description: str             # Brief description
    techstack: str              # Technology stack
    features: list[str]         # List of features
    files: list[File]           # Required files
```

#### `ImplementationTask`
```python
class ImplementationTask(BaseModel):
    filepath: str               # Target file path
    task_description: str       # Detailed task description
```

#### `CoderState`
```python
class CoderState(BaseModel):
    task_plan: TaskPlan                    # Implementation plan
    current_step_idx: int                  # Current step index
    current_file_content: Optional[str]    # Current file content
```

### Tool Functions

#### File Operations
```python
@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file within the project root."""

@tool  
def read_file(path: str) -> str:
    """Reads content from a file within the project root."""

@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory."""

@tool
def get_current_directory() -> str:
    """Returns the current working directory."""
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Groq API Key Issues
**Problem**: `AuthenticationError` or `Invalid API key`  
**Solution**:
```bash
# Check if .env file exists and has correct format
cat .env
# Should show: GROQ_API_KEY=your_actual_key_here

# Verify API key is valid at groq.com
# Regenerate if necessary
```

#### 2. Import Errors
**Problem**: `ModuleNotFoundError` for project modules  
**Solution**:
```bash
# Ensure you're in the project root directory
pwd
# Should end with: /lovable-clone

# Run with UV to ensure correct environment
uv run main.py
```

#### 3. File Permission Errors
**Problem**: `PermissionError` when writing files  
**Solution**:
```bash
# Check directory permissions
ls -la agent/
# Ensure generated_project directory is writable
chmod 755 agent/generated_project/
```

#### 4. Recursion Limit Exceeded
**Problem**: `RecursionError` during complex project generation  
**Solution**:
```bash
# Increase recursion limit
uv run main.py --recursion-limit 200
```

## 🤝 Contributing Guidelines

### Development Workflow

1. **Fork and Clone**
   ```bash
   git clone <your-fork-url>
   cd lovable-clone
   ```

2. **Set Up Development Environment**
   ```bash
   uv sync
   uv add --dev pytest black flake8 mypy
   ```

3. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes and Test**
   ```bash
   # Run tests
   uv run pytest
   
   # Format code
   uv run black .
   
   # Type checking
   uv run mypy .
   ```

### Areas for Contribution

1. **Additional LLM Providers**: Support for OpenAI, Anthropic, etc.
2. **Enhanced Tools**: Database tools, API integration tools
3. **UI Improvements**: Web interface for the application
4. **Testing Framework**: Comprehensive test suite
5. **Performance Optimization**: Caching, parallel processing

## 📖 Learning Insights

### Key Concepts Demonstrated

#### 1. Agentic AI Architecture
This project demonstrates how to build **multi-agent systems** where:
- Each agent has a specific, well-defined role
- Agents communicate through structured data formats
- The system maintains state across agent interactions
- Complex tasks are broken down into manageable steps

#### 2. Structured LLM Outputs
Using **Pydantic schemas** with LLMs provides:
- Reliable, parseable responses
- Type safety and validation
- Clear contracts between system components
- Reduced error handling complexity

#### 3. Tool-Using Agents
The **ReAct pattern** (Reasoning + Acting) enables:
- LLMs to interact with external systems
- Dynamic decision-making during execution
- Self-correction and iterative improvement
- Real-world problem solving beyond text generation

### Reusable Patterns

#### 1. Agent Factory Pattern
```python
def create_agent(llm, tools, system_prompt):
    """Reusable pattern for creating tool-using agents."""
    return create_react_agent(llm, tools, system_prompt)
```

#### 2. Schema-Driven Development
```python
class TaskSchema(BaseModel):
    """Define data structures first, then build logic around them."""
    task_type: str
    parameters: dict
    expected_output: str
```

#### 3. Safe File Operations
```python
def safe_path_operation(base_path, requested_path):
    """Always validate paths to prevent security issues."""
    resolved = (base_path / requested_path).resolve()
    if base_path not in resolved.parents:
        raise SecurityError("Path traversal attempt")
    return resolved
```

### Applications Beyond This Project

The patterns and concepts in this project can be applied to:

- **Content Management Systems**: Multi-agent content creation and editing
- **DevOps Automation**: Infrastructure provisioning and management
- **Data Processing Pipelines**: ETL workflows with AI-driven transformations
- **Customer Service Systems**: Multi-step problem resolution workflows
- **Educational Platforms**: Personalized learning path generation

---

## 🎉 Conclusion

This Lovable Clone demonstrates that building sophisticated AI applications requires careful attention to:

- **Architecture**: Well-designed agent interactions and state management
- **Reliability**: Robust error handling and structured outputs
- **Usability**: Clear interfaces and comprehensive documentation
- **Maintainability**: Clean code organization and testing strategies

The project serves as both a functional application and a learning resource for anyone interested in building agentic AI systems. Whether you're exploring AI application development or looking to understand how platforms like Lovable might work under the hood, this codebase provides practical insights and reusable patterns.

**Happy coding!** 🚀

---

*For questions, issues, or contributions, please refer to the troubleshooting section or create an issue in the repository.*
