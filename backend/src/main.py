from fastapi import FastAPI
from src.modules.users.router import router as user_router
from src.modules.crm_agent.router.router import router as agent_router

app = FastAPI(
    title="CRM API",
    description="API for CRM system with user data management",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(agent_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to CRM API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
