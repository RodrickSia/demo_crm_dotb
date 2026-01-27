API_BASE_URL = "http://127.0.0.1:8000"

ENDPOINTS_CONFIG = [
    {"name": "Journey", "endpoint": "Journey"},
    {"name": "Calls", "endpoint": "Calls"},
    {"name": "Attendance", "endpoint": "attendance"},
    {"name": "Enrollments", "endpoint": "enrollments"},
    {"name": "Meetings", "endpoint": "meetings"},
    {"name": "Notes", "endpoint": "notes"},
    {"name": "Receipts", "endpoint": "receipts"},
    {"name": "Tasks", "endpoint": "tasks"},
]

# Follow-up action colors based on enrollment conversion priority
FOLLOWUP_ACTION_COLORS = {
    "Send Welcome Email": "#3b82f6",  # Blue - initial contact
    "Schedule Discovery Call": "#8b5cf6",  # Purple - qualification
    "Share Program Information": "#06b6d4",  # Cyan - education
    "Invite to Open House/Campus Tour": "#10b981",  # Green - engagement
    "Send Personalized Enrollment Proposal": "#f59e0b",  # Orange - high priority conversion
    "Follow Up on Pending Application": "#ef4444",  # Red - urgent enrollment action
    "Schedule Assessment/Placement Test": "#14b8a6",  # Teal - concrete next step
    "Offer Trial Class/Demo Session": "#22c55e",  # Medium green - experience value
    "Send Re-Engagement Campaign": "#f97316",  # Orange-red - reactivation
    "Request Referral/Testimonial": "#ec4899"  # Pink - lead generation
}
