from fastapi import APIRouter, HTTPException, Query
from typing import Literal, Any, Optional
from src.modules.users.service import user_service
from ..graph.state import AgentState, UserState, WeightedAtributes
from ..graph.graph import graph

router = APIRouter(prefix="/user/llm", tags=["agent"])

def get_all_data_by_user_id(user_id: str) -> AgentState:
    """Helper to fetch all required user data for the agent."""
    journey_id = user_service.get_journey_id_by_student_id(user_id)
    
    calls_res = user_service.get_calls_by_user_id(user_id)
    calls = calls_res[0] if isinstance(calls_res, list) and len(calls_res) > 0 else None
    notes_res = user_service.get_notes_by_user_id(user_id)
    notes = notes_res[0] if isinstance(notes_res, list) and len(notes_res) > 0 else None
    receipts_res = user_service.get_receipts_by_user_id(user_id)
    receipts = receipts_res[0] if isinstance(receipts_res, list) and len(receipts_res) > 0 else None
    tasks_res = user_service.get_tasks_by_user_id(user_id)
    tasks = tasks_res[0] if isinstance(tasks_res, list) and len(tasks_res) > 0 else None
    meetings_res = user_service.get_meetings_by_user_id(user_id)
    meetings = meetings_res[0] if isinstance(meetings_res, list) and len(meetings_res) > 0 else None
    attendance_res = user_service.get_attendance_by_user_id(user_id)
    attendance = attendance_res[0] if isinstance(attendance_res, list) and len(attendance_res) > 0 else None
    enrollments_res = user_service.get_enrollments_by_user_id(user_id)
    enrollments = enrollments_res[0] if isinstance(enrollments_res, list) and len(enrollments_res) > 0 else None

    user_data = AgentState(
        user = UserState(
            user_id=user_id,
            journey_id=str(journey_id),
            calls=calls,
            notes=notes,
            receipts=receipts,
            tasks=tasks,
            meetings=meetings,
            attendance=attendance,
            enrollments=enrollments
        ),
        intent="Unknown"
    )
    return user_data

@router.get("/{user_id}/score")
def get_lead_score(
    user_id: str,
    demographics: float = Query(0.1, ge=0, le=1),
    acedemic_background: float = Query(0.2, ge=0, le=1),
    activities_history: float = Query(0.2, ge=0, le=1),
    payment_history: float = Query(0.3, ge=0, le=1),
    learning_history: float = Query(0.2, ge=0, le=1)
) -> Any:
    """Generate AI lead score for a user."""
    weights = WeightedAtributes(
        demographics=demographics,
        acedemic_background=acedemic_background,
        activities_history=activities_history,
        payment_history=payment_history,
        learning_history=learning_history
    )
    
    total_weight = demographics + acedemic_background + activities_history + payment_history + learning_history
    if not (0.99 <= total_weight <= 1.01):
        raise HTTPException(
            status_code=400,
            detail=f"Weights must sum to 1.0. Current sum: {total_weight:.2f}"
        )
    
    state = get_all_data_by_user_id(user_id)
    state.intent = "score"
    state.weights = weights
    return graph.invoke(state)

@router.get("/{user_id}/activity_summary")
def get_activity_summary(user_id: str) -> Any:
    """Generate AI activity summary for a user."""
    state = get_all_data_by_user_id(user_id)
    state.intent = "activity_summary"
    return graph.invoke(state)

@router.get("/{user_id}/stage")
def get_followup_action(user_id: str) -> Any:
    """Determine AI-recommended next follow-up action (stage)."""
    state = get_all_data_by_user_id(user_id)
    state.intent = "stage"
    return graph.invoke(state)

# Keep the generic route for backward compatibility with older frontend calls if any
@router.get("/{user_id}/{intent}")
def get_agent_response(
    user_id: str, 
    intent: Literal["score", "stage", "activity_summary"],
    demographics: float = Query(0.1, ge=0, le=1),
    acedemic_background: float = Query(0.2, ge=0, le=1),
    activities_history: float = Query(0.2, ge=0, le=1),
    payment_history: float = Query(0.3, ge=0, le=1),
    learning_history: float = Query(0.2, ge=0, le=1)
) -> Any:
    """Generic AI-powered insight endpoint."""
    if intent == "score":
        return get_lead_score(user_id, demographics, acedemic_background, activities_history, payment_history, learning_history)
    elif intent == "activity_summary":
        return get_activity_summary(user_id)
    elif intent == "stage":
        return get_followup_action(user_id)
    else:
        raise HTTPException(status_code=400, detail="Invalid intent")
