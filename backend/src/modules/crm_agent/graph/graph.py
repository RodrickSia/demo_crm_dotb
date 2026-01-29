from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import (
    classifying_intent,
    generate_lead_score,
    generate_followup_action,
    generate_activity_summary,
    generate_lead_score_deepagent
)

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("classifying_intent", classifying_intent)
workflow.add_node("generate_lead_score", generate_lead_score_deepagent)
workflow.add_node("generate_followup_action", generate_followup_action)
workflow.add_node("generate_activity_summary", generate_activity_summary)

# Add edges
workflow.add_edge(START, "classifying_intent")
graph = workflow.compile()
