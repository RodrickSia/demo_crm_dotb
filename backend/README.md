# CRM DOTB - Backend API


This is the FastAPI-based backend for the CRM DOTB system.

## 🏗️ Structure

- **`src/main.py`**: The entry point for the FastAPI application.
- **`src/modules/`**: Contains the business logic modules.
    - `users/`: User data and service layer.
    - `crm_agent/`: LangGraph reasoning engine and AI logic.
- **`src/shared/`**: Common utilities.
- **`src/config/`**: Global database and system settings.


## 🏃 Running the Backend

1. Create a `.env` file in the `backend` directory with the following secrets (replace values as needed):
    ```env
    SECRET_KEY=your_secret_key
    DB_PASSWORD=your_db_password
    API_TOKEN=your_api_token
    ```

2. Build and run the backend using Docker Compose:
    ```bash
    docker compose up --build
    ```

Visit the API documentation at `http://127.0.0.1:8000/docs`.
