

def planner_prompt(user_prompt: str) -> str:

    Planner_prompt = f"""You are a planner agent. convert the user prompt into a COMPLETE engineering project plan.
                    User prompt: {user_prompt}
                    """
    return Planner_prompt   

