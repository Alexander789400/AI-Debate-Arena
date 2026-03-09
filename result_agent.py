from llm import result_llm


def result_agent(state):

    history = "\n".join(state["history"])

    prompt = f"""
You are the final judge of a debate.

Debate history:
{history}

Decide the overall winner.

Rules:
- Choose PRO or CON
- Explain briefly in 40 words
"""

    response = result_llm.invoke(prompt)

    result = response.content

    state["final_result"] = result

    return state