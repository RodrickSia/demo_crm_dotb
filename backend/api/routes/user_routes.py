from fastapi import APIRouter, HTTPException, Query
from typing import List, Any, Literal, Optional
from services.CRMAgent.utils.state import AgentState, UserState, WeightedAtributes
from services.CRMAgent.agent import graph
from services.user_service import user_service

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/{user_id}")
def get_student_by_id(user_id: str):
    return user_service.get_student_by_id(user_id)


def get_all_data_by_user_id(user_id: str) -> AgentState:
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
@router.get("/llm/{user_id}/{intent}")
def get_agent_response(
    user_id: str, 
    intent: Literal["score", "stage", "activity_summary"],
    demographics: float = Query(0.1, ge=0, le=1),
    acedemic_background: float = Query(0.2, ge=0, le=1),
    activities_history: float = Query(0.2, ge=0, le=1),
    payment_history: float = Query(0.3, ge=0, le=1),
    learning_history: float = Query(0.2, ge=0, le=1)
) -> Any:
    """
    Get AI-powered insights for a user.
    
    Args:
        user_id: The student ID
        intent: Must be one of: "score", "stage", or "activity_summary"
        demographics: Weight for demographics (0-1)
        acedemic_background: Weight for academic background (0-1)
        activities_history: Weight for activities history (0-1)
        payment_history: Weight for payment history (0-1)
        learning_history: Weight for learning history (0-1)
    
    Note: For "score" intent, weights should sum to 1.0
    
    Returns:
        AgentState with the requested insight populated
    """
    # Validate intent
    valid_intents = ["score", "stage", "activity_summary"]
    if intent not in valid_intents:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid intent. Must be one of: {', '.join(valid_intents)}"
        )
    
    # For score intent, validate weights sum to 1.0
    if intent == "score":
        weights = WeightedAtributes(
            demographics=demographics,
            acedemic_background=acedemic_background,
            activities_history=activities_history,
            payment_history=payment_history,
            learning_history=learning_history
        )
        
        total_weight = (
            demographics +
            acedemic_background +
            activities_history +
            payment_history +
            learning_history
        )
        
        if not (0.99 <= total_weight <= 1.01):  # Allow small floating point tolerance
            raise HTTPException(
                status_code=400,
                detail=f"Weights must sum to 1.0. Current sum: {total_weight:.2f}"
            )
    else:
        weights = None
    
    state = get_all_data_by_user_id(user_id)
    state.intent = intent
    state.weights = weights
    response = graph.invoke(state)
    return response

@router.get("/")
def get_all_students():
    return user_service.get_all_students()


@router.get("/Journey/{user_id}")
def get_journeys_by_user_id(user_id: str) -> List[Any]:
    return user_service.get_journeys_by_user_id(user_id)


@router.get("/attendance/{user_id}")
def get_attendance_by_user_id(user_id: str) -> List[Any]:
    return user_service.get_attendance_by_user_id(user_id)


@router.get("/enrollments/{user_id}")
def get_enrollments_by_user_id(user_id: str) -> List[Any]:
    return user_service.get_enrollments_by_user_id(user_id)


@router.get("/meetings/{user_id}")
def get_meetings_by_user_id(user_id: str) -> List[Any]:
    return user_service.get_meetings_by_user_id(user_id)


@router.get("/notes/{user_id}")
def get_notes_by_user_id(user_id: str) -> List[Any]:
    return user_service.get_notes_by_user_id(user_id)


@router.get("/receipts/{user_id}")
def get_receipts_by_user_id(user_id: str) -> List[Any]:
    return user_service.get_receipts_by_user_id(user_id)


@router.get("/tasks/{user_id}")
def get_tasks_by_user_id(user_id: str) -> List[Any]:
    return user_service.get_tasks_by_user_id(user_id)


@router.get("/Calls/{user_id}")
def get_calls_by_user_id(user_id: str) -> List[Any]:
    return user_service.get_calls_by_user_id(user_id)
