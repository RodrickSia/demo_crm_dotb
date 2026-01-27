# CRM DOTB - Backend API

This is the FastAPI-based backend for the CRM DOTB system. It follows a modular monolith architecture.

## 🏗️ Structure

- **`src/main.py`**: The entry point for the FastAPI application.
- **`src/modules/`**: Contains the business logic modules.
    - `users/`: User data and service layer.
    - `crm_agent/`: LangGraph reasoning engine and AI logic.
- **`src/shared/`**: Common utilities.
- **`src/config/`**: Global database and system settings.

## 🏃 Running the Backend

```bash
conda activate backend
cd backend
python -m src.main
```

Visit the API documentation at `http://127.0.0.1:8000/docs`.

For full project documentation, including setup and architecture, please refer to the [Root README](../README.md).
