from langgraph.graph import StateGraph, END

from state import DebateState

from agents.planner import planner_agent
from agents.pro_agent import pro_agent
from agents.con_agent import con_agent
from agents.judge_agent import judge_agent
from agents.result_agent import result_agent


def should_continue(state: DebateState):

    if state["round"] < 2:
        state["round"] += 1
        return "pro"

    return "result"


def build_graph():

    workflow = StateGraph(DebateState)

    # nodes
    workflow.add_node("planner", planner_agent)
    workflow.add_node("pro", pro_agent)
    workflow.add_node("con", con_agent)
    workflow.add_node("judge", judge_agent)
    workflow.add_node("result", result_agent)

    # edges
    workflow.set_entry_point("planner")

    workflow.add_edge("planner", "pro")
    workflow.add_edge("pro", "con")
    workflow.add_edge("con", "judge")

    workflow.add_conditional_edges(
        "judge",
        should_continue,
        {
            "pro": "pro",
            "result": "result"
        }
    )

    workflow.add_edge("result", END)

    return workflow.compile()

graph = build_graph()


def run_debate(topic):

    transcript = []

    state = {
        "topic": topic,
        "history": [],
        "pro_argument": "",
        "con_argument": "",
        "judge_result": "",
        "final_result": "",
        "round": 1
    }

    for step in graph.stream(state):

        for node, data in step.items():

            if node == "judge":

                transcript.append({
                    "round": data["round"],
                    "pro": data["pro_argument"],
                    "con": data["con_argument"],
                    "judge": data["judge_result"]
                })

            if node == "result":

                final = data["final_result"]

    return transcript, final