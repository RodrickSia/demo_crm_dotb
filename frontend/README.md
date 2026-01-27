# CRM DOTB - Frontend

This is the Streamlit-based frontend for the CRM DOTB system. It has been refactored into a modular structure located in the `src/` directory.

## 🏗️ Structure

- **`main.py`**: The entry point for the Streamlit application.
- **`pages/`**: Contains the page navigation shims.
- **`src/`**: The core modular logic.
    - `modules/`: Feature-specific views and components (Users, Profile, CRM).
    - `shared/`: Shared API logic, UI styles, and configurations.

## 🏃 Running the Frontend

Ensure the backend is running first!

```bash
cd frontend
streamlit run main.py
```

For full project documentation, including setup and architecture, please refer to the [Root README](../README.md).
