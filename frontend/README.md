# Frontend Structure

This frontend application has been refactored into a modular structure for better maintainability and reusability.

## Directory Structure

```
frontend/
├── main.py                      # Entry point / Dashboard
├── requirements.txt             # Dependencies
├── pages/                       # Streamlit pages
│   ├── User_Profile.py         # Original user profile page
│   ├── User_Profile_Refactored.py  # Refactored version
│   ├── Users.py                # Original users list page
│   └── Users_Refactored.py     # Refactored version
├── components/                  # Reusable UI components
│   ├── __init__.py
│   ├── styles.py               # CSS styles
│   ├── lead_score_card.py      # Lead score display component
│   ├── activity_summary_card.py # Activity summary component
│   ├── lead_stage_card.py      # Lead stage component
│   ├── user_components.py      # User-related UI components
│   └── users_components.py     # Users list UI components
├── services/                    # API and business logic
│   ├── __init__.py
│   └── api_service.py          # All API calls
└── utils/                       # Configuration and utilities
    ├── __init__.py
    └── config.py               # App configuration
```

## Components Overview

### `/components/`
Reusable UI components that can be used across different pages:
- **styles.py**: Contains CSS styling for action cards
- **lead_score_card.py**: Renders the circular lead score indicator
- **activity_summary_card.py**: Renders the activity summary card
- **lead_stage_card.py**: Renders the lead stage indicator
- **user_components.py**: User profile related components (selector, basic info, data tabs, summary)
- **users_components.py**: Users list page components (metrics, search, filters, export)

### `/services/`
Business logic and API communication:
- **api_service.py**: All API calls centralized here
  - `fetch_all_students()`: Get all students
  - `fetch_user_data()`: Get user-specific data by endpoint
  - `fetch_lead_score()`: Get lead scoring (placeholder)
  - `fetch_activity_summary()`: Get activity summary (placeholder)
  - `fetch_lead_stage()`: Get lead stage (placeholder)

### `/utils/`
Configuration and helper utilities:
- **config.py**: Application configuration
  - `API_BASE_URL`: Backend API URL
  - `ENDPOINTS_CONFIG`: List of all data endpoints
  - `LEAD_STAGE_COLORS`: Color mapping for lead stages

## Benefits of This Structure

1. **Modularity**: Each component has a single responsibility
2. **Reusability**: Components can be reused across different pages
3. **Maintainability**: Easy to locate and update specific functionality
4. **Testability**: Components can be tested independently
5. **Scalability**: Easy to add new components or pages

## Usage

### Using Refactored Pages
The refactored pages (`User_Profile_Refactored.py` and `Users_Refactored.py`) use the modular components.

### Adding New Components
1. Create a new file in `/components/`
2. Define your component as a function
3. Import and use in your page

Example:
```python
# components/my_component.py
import streamlit as st

def render_my_component(data):
    st.write(data)

# pages/My_Page.py
from components.my_component import render_my_component

render_my_component("Hello World")
```

### Adding New API Endpoints
Add your API function to `services/api_service.py`:
```python
@st.cache_data(ttl=60)
def fetch_new_data(param):
    response = requests.get(f"{API_BASE_URL}/new-endpoint/{param}")
    return response.json()
```

## Running the Application

```bash
cd frontend
streamlit run main.py
```

The app will be available at `http://localhost:8501`
