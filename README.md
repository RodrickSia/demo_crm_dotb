# CRM DOTB - AI-Powered Modular CRM


A modern CRM system featuring AI-driven insights for lead management.

## 🚀 Project Overview

CRM DOTB is designed to manage student relationships for educational institutions. It provides a comprehensive dashboard for user data management, integrated with a powerful AI agent that generates lead scores, activity summaries, and recommended next steps using **LangGraph** and **Google Gemini**.




### Backend Structure (`/backend/src`)
- **`modules/users`**: Core user data management (Student profiles, journeys, attendance, etc.).
- **`modules/crm_agent`**: AI reasoning engine built with LangGraph.
   - `graph/`: LangGraph definition (nodes, state, graph).
   - `config/`: AI-specific prompts and configuration.
- **`shared/`**: Global utilities and helpers.
- **`config/`**: Database and system-wide settings.

### Frontend Structure (`/frontend/src`)
- **`modules/users`**: User listing and search views.
- **`modules/profile`**: Detailed student profile visualization.
- **`modules/crm`**: AI insight cards and interaction components.
- **`shared/`**: API clients, UI components, and global styles.

## 🛠️ Tech Stack

- **Backend**: Python 3.13, FastAPI, LangGraph, LangChain, Google Gemini API, Supabase (PostgreSQL).
- **Frontend**: Streamlit, Pandas, Requests.
- **Infrastructure**: Conda for environment management.


## ⚙️ Setup & Installation

### Backend Setup
1. Create a `.env` file in the `backend` directory with the following secrets (replace values as needed):
   ```env
   SECRET_KEY=your_secret_key
   DB_PASSWORD=your_db_password
   API_TOKEN=your_api_token
   ```
2. Build and run the backend using Docker Compose:
   ```bash
   cd backend
   docker compose up --build
   ```
   The API will be available at `http://127.0.0.1:8000`. You can visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

### Frontend Setup
1. Ensure you have the necessary requirements for Streamlit:
   ```bash
   cd frontend
   pip install -r requirements.txt
   ```


## 🏃 Running the Application

### 1. Start the Backend API
See the Backend Setup section above for Docker Compose instructions.

### 2. Start the Frontend
```bash
cd frontend
streamlit run main.py
```
The dashboard will open in your browser at `http://localhost:8501`.

## 🧠 AI Features
The AI Agent utilizes LangGraph to:
1. **Classify Intent**: Routes requests based on user needs (Score vs. Summary vs. Action).
2. **Lead Scoring**: Evaluates prospects based on weighted attributes (Demographics, Academic, Activities, Payment, Learning).
3. **Activity Summarization**: Generates professional summaries of a student's history.
4. **Follow-up Suggestions**: Recommends the best next step to advance the lead.

## 📂 Repository Structure
```
CRM_DOTB/
├── backend/
│   ├── src/
│   │   ├── modules/         # Business domain modules
│   │   ├── shared/          # Shared utilities
│   │   ├── config/          # Global configuration
│   │   └── main.py          # Entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── modules/         # Frontend feature modules
│   │   ├── shared/          # Common UI and API logic
│   │   └── main_view.py     # Main dashboard logic
│   ├── pages/               # Streamlit page entry points
│   ├── main.py              # App entry point
│   └── requirements.txt
└── README.md                # This file
```
