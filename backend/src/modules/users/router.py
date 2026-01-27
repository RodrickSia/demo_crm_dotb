from fastapi import APIRouter, HTTPException, Query
from typing import List, Any
from .service import user_service

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/{user_id}")
def get_student_by_id(user_id: str):
    return user_service.get_student_by_id(user_id)


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
