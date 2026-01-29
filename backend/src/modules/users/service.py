from typing import List, Any
from src.config.database import get_db_client
from src.config.settings import TABLES
from src.shared.utils.helpers import extract_response_data


class UserService:
    def __init__(self):
        self.client = get_db_client()
    
    def get_journey_id_by_student_id(self, user_id: str) -> str:
        resp = self.client.table(TABLES["JOURNEY"]).select("id").eq("student_id", user_id).execute()
        journeys = extract_response_data(resp)
        if not journeys:
            raise Exception("No journeys found for the given student ID")
        return journeys[0]["id"]
    
    def get_student_by_id(self, user_id: str) -> Any:
        response = self.client.table(TABLES["STUDENT"]).select("*").eq("id", user_id).execute()
        return response.data
    
    def get_all_students(self) -> Any:
        response = self.client.table(TABLES["STUDENT"]).select("*").execute()
        return response.data
    
    def get_journeys_by_user_id(self, user_id: str) -> List[Any]:
        response = self.client.table(TABLES["JOURNEY"]).select("*").eq("student_id", user_id).execute()
        return extract_response_data(response)

    def get_data_by_journey_id(self, journey_id: str, table_key: str) -> List[Any]:
        response = self.client.table(TABLES[table_key]).select("*").eq("journey_id", journey_id).execute()
        return extract_response_data(response)

    def get_full_user_state(self, user_id: str) -> dict:
        journey_id = self.get_journey_id_by_student_id(user_id)
        
        mapping = {
            "calls": "CALLS",
            "attendance": "ATTENDANCE",
            "enrollments": "ENROLLMENTS",
            "meetings": "MEETINGS",
            "notes": "NOTES",
            "receipts": "RECEIPTS",
            "tasks": "TASKS"
        }

        state_data = {"user_id": user_id, "journey_id": str(journey_id)}
        for field, table_key in mapping.items():
            res = self.get_data_by_journey_id(journey_id, table_key)
            state_data[field] = res[0] if res else None
            
        return state_data

    def get_attendance_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        return self.get_data_by_journey_id(journey_id, "ATTENDANCE")
    
    def get_enrollments_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        return self.get_data_by_journey_id(journey_id, "ENROLLMENTS")
    
    def get_meetings_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        return self.get_data_by_journey_id(journey_id, "MEETINGS")
    
    def get_notes_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        return self.get_data_by_journey_id(journey_id, "NOTES")
    
    def get_receipts_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        return self.get_data_by_journey_id(journey_id, "RECEIPTS")
    
    def get_tasks_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        return self.get_data_by_journey_id(journey_id, "TASKS")
    
    def get_calls_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        return self.get_data_by_journey_id(journey_id, "CALLS")


user_service = UserService()
