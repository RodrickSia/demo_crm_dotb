from typing import List, Any
from config.database import get_db_client
from config.settings import TABLES
from utils.helpers import extract_response_data


class UserService:
    def __init__(self):
        self.client = get_db_client()
    
    def get_journey_id_by_student_id(self, user_id: str) -> str:
        resp = self.client.table(TABLES[1]).select("id").eq("student_id", user_id).execute()
        journeys = extract_response_data(resp)
        
        if not journeys:
            raise Exception("No journeys found for the given student ID")
        
        first_journey = journeys[0]
        if not isinstance(first_journey, dict) or "id" not in first_journey:
            raise Exception("Invalid journey data format")
        
        return first_journey["id"]
    
    def get_student_by_id(self, user_id: str) -> Any:
        response = self.client.table("Student").select("*").eq("id", user_id).execute()
        return response.data
    
    def get_all_students(self) -> Any:
        response = self.client.table("Student").select("*").execute()
        return response.data
    
    def get_journeys_by_user_id(self, user_id: str) -> List[Any]:
        response = self.client.table(TABLES[1]).select("*").eq("student_id", user_id).execute()
        return extract_response_data(response)
    
    def get_attendance_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        response = self.client.table(TABLES[3]).select("*").eq("journey_id", journey_id).execute()
        return extract_response_data(response)
    
    def get_enrollments_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        response = self.client.table(TABLES[4]).select("*").eq("journey_id", journey_id).execute()
        return extract_response_data(response)
    
    def get_meetings_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        response = self.client.table(TABLES[5]).select("*").eq("journey_id", journey_id).execute()
        return extract_response_data(response)
    
    def get_notes_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        response = self.client.table(TABLES[6]).select("*").eq("journey_id", journey_id).execute()
        return extract_response_data(response)
    
    def get_receipts_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        response = self.client.table(TABLES[7]).select("*").eq("journey_id", journey_id).execute()
        return extract_response_data(response)
    
    def get_tasks_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        response = self.client.table(TABLES[8]).select("*").eq("journey_id", journey_id).execute()
        return extract_response_data(response)
    
    def get_calls_by_user_id(self, user_id: str) -> List[Any]:
        journey_id = self.get_journey_id_by_student_id(user_id)
        response = self.client.table(TABLES[0]).select("*").eq("journey_id", journey_id).execute()
        return extract_response_data(response)


user_service = UserService()
