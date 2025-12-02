from services.CRMAgent.agent import graph
from services.CRMAgent.utils.state import AgentState

def get_agent_response(state: AgentState, intent: str) -> str:
    state.intent = intent
    config = {"configurable": {"thread_id": f"{state.user.user_id}"}}
    response = graph.invoke(state)
    
    if intent == "score":
        return f"Lead Score: {response["lead_score"]}"
    elif intent == "stage":
        return f"Lead Stage: {response["lead_stage"]}"
    elif intent == "activity_summary":
        return f"Activity Summary: {response["activity_summary"]}"
    else:
        raise ValueError("Invalid intent provided.")