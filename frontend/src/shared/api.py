import requests
import streamlit as st
from .config import API_BASE_URL


@st.cache_data(ttl=60)
def fetch_all_students():
    try:
        response = requests.get(f"{API_BASE_URL}/user")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch students: {e}")
        return []


@st.cache_data(ttl=60)
def fetch_user_data(user_id, endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}/user/{endpoint}/{user_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return []


def fetch_lead_score(user_id, weights=None):
    """
    Fetch AI-generated lead score for a user.
    Intent: "score"
    
    Args:
        user_id: The student ID
        weights: Optional dict with keys: demographics, acedemic_background, 
                 activities_history, payment_history, learning_history
    """
    try:
        url = f"{API_BASE_URL}/user/llm/{user_id}/score"
        
        # Add weights as query parameters if provided
        if weights:
            params = {
                'demographics': weights.get('demographics', 0.1),
                'acedemic_background': weights.get('acedemic_background', 0.2),
                'activities_history': weights.get('activities_history', 0.2),
                'payment_history': weights.get('payment_history', 0.3),
                'learning_history': weights.get('learning_history', 0.2)
            }
            response = requests.get(url, params=params)
        else:
            response = requests.get(url)
            
        response.raise_for_status()
        data = response.json()
        return {
            "score": data.get("lead_score", 0),
            "explanation": data.get("lead_score_explanation", "No explanation available.")
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch lead score: {e}")
        return {"score": 0, "explanation": "Failed to fetch explanation."}


def fetch_activity_summary(user_id):
    """
    Fetch AI-generated activity summary for a user.
    Intent: "activity_summary"
    """
    try:
        response = requests.get(f"{API_BASE_URL}/user/llm/{user_id}/activity_summary")
        response.raise_for_status()
        data = response.json()
        summary_text = data.get("activity_summary", "")
        explanation_text = data.get("activity_summary_explanation", "")
        
        return {
            "summary": summary_text,
            "explanation": explanation_text
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch activity summary: {e}")
        return {
            "summary": "Failed to generate summary",
            "explanation": "Failed to fetch insights."
        }


def fetch_followup_action(user_id):
    """
    Fetch AI-generated follow-up action for a user.
    Intent: "stage"
    """
    try:
        response = requests.get(f"{API_BASE_URL}/user/llm/{user_id}/stage")
        response.raise_for_status()
        data = response.json()
        return {
            "action": data.get("followup_action", "Unknown"),
            "explanation": data.get("followup_action_explanation", "No explanation available.")
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch follow-up action: {e}")
        return {"action": "Unknown", "explanation": "Failed to fetch explanation."}
