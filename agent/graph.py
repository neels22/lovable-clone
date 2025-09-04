
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from prompts import planner_prompt,architect_prompt,coder_system_prompt
from states import Plan,TaskPlan,CoderState
from langgraph.graph import StateGraph, START, END
from langchain.globals import set_debug, set_verbose
from tools import read_file, write_file, list_files, get_current_directory
from langgraph.prebuilt import create_react_agent
load_dotenv()


# set_debug(True)
# set_verbose(True)


llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"))


# result = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))

# print(result)

def planner_agent(state: dict) -> dict:
    user_prompt = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    plan = state["plan"]
    resp = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan))
    if resp is None:
        raise ValueError("No task plan found")
    resp.plan = plan # here the plan is added to keep the context going on forward possible because configdict allowed extra
    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]
    
    try:
        # Fix: Use proper tool invocation
        existing_content = read_file.invoke({"path": current_task.filepath})
    except Exception as e:
        print(f"Error reading file {current_task.filepath}: {e}")
        existing_content = ""

    system_prompt = coder_system_prompt()
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )

    coder_tools = [read_file, write_file, list_files, get_current_directory]
    react_agent = create_react_agent(llm, coder_tools)

    try:
        # Fix: Capture and handle the result
        result = react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                                 {"role": "user", "content": user_prompt}]})
        
        # Only increment step if successful
        coder_state.current_step_idx += 1
        return {"coder_state": coder_state, "status": "STEP_COMPLETED", "result": result}
        
    except Exception as e:
        print(f"Error executing coder agent for step {coder_state.current_step_idx}: {e}")
        return {"coder_state": coder_state, "status": "ERROR", "error": str(e)}





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

graph.set_entry_point("planner")
agent = graph.compile()
if __name__ == "__main__":
    result = agent.invoke({"user_prompt": "Build a colourful modern calculator app in html css and js"},
                          {"recursion_limit": 100})
    print("Final State:", result)
