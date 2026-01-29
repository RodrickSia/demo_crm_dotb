from pydantic import BaseModel
from typing import Optional

class UserState(BaseModel):
    user_id: str
    journey_id: Optional[str] = None
    calls: Optional[dict] = None
    notes: Optional[dict] = None
    receipts: Optional[dict] = None
    tasks: Optional[dict] = None
    meetings: Optional[dict] = None
    attendance: Optional[dict] = None
    enrollments: Optional[dict] = None
    
class WeightedAtributes(BaseModel):
    demographics: float = 0.1
    acedemic_background: float = 0.2
    activities_history: float = 0.2
    payment_history: float = 0.3
    learning_history: float = 0.3

class AgentState(BaseModel):
    user: UserState
    intent: str = "Unknown"
    lead_score: int = 0
    followup_action: str = "Unknown"
    activity_summary: str = ""
    # Weighted attributes for lead scoring
    weights: WeightedAtributes
    # Explanations for each LLM-generated insight
    lead_score_explanation: str = ""
    followup_action_explanation: str = ""
    activity_summary_explanation: str = ""
