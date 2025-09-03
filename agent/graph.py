
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from prompts import planner_prompt,architect_prompt
from states import Plan,TaskPlan
from langgraph.graph import StateGraph, START, END
load_dotenv()





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


graph = StateGraph(dict)
graph.add_node("planner",planner_agent)
graph.add_node("architect",architect_agent) 
graph.add_edge("planner","architect")
graph.set_entry_point("planner")


agent = graph.compile()
user_prompt = "create a simple calculator web application"
result = agent.invoke({"user_prompt": user_prompt})
print(result)


