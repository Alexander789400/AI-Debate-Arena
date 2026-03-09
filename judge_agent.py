from llm import judge_llm


def judge_agent(state):

    pro = state["pro_argument"]
    con = state["con_argument"]
    round_no = state["round"]

    prompt = f"""
You are a neutral debate judge.

PRO Argument:
{pro}

CON Argument:
{con}

Evaluate round {round_no}.

Rules:
- Maximum 50 words
- State which side was stronger.
"""

    response = judge_llm.invoke(prompt)

    result = response.content

    state["judge_result"] = result
    state["history"].append(f"JUDGE Round {round_no}: {result}")

    return state