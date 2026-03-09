from llm import pro_llm
from tools.search_tools import search_tool


def pro_agent(state):

    topic = state["topic"]
    round_no = state["round"]

    # search supporting evidence
    evidence = search_tool(f"arguments supporting {topic}")
    evidence = evidence[:500]

    prompt = f"""
You are the PRO side in a debate.

Topic:
{topic}

Research Evidence:
{evidence}

Task:
Create a strong supporting argument for round {round_no}.

Rules:
- Maximum 60 words
- Logical and persuasive
"""

    response = pro_llm.invoke(prompt)
    result = response.content

    state["pro_argument"] = result
    state["history"].append(f"PRO Round {round_no}: {result}")

    return state