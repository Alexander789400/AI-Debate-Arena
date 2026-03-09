from llm import con_llm
from tools.search_tools import search_tool


def con_agent(state):

    topic = state["topic"]
    pro_arg = state["pro_argument"]
    round_no = state["round"]

    # Search evidence
    evidence = search_tool(f"arguments against {topic}")
    evidence = evidence[:500]

    prompt = f"""
You are the CON side in a debate.

Topic:
{topic}

Opponent Argument:
{pro_arg}

Research Evidence:
{evidence}

Task:
Provide a strong counter argument for Round {round_no}.

Rules:
- Maximum 60 words
- Be clear and logical
"""

    response = con_llm.invoke(prompt)

    result = response.content

    state["con_argument"] = result
    state["history"].append(f"CON Round {round_no}: {result}")

    return state