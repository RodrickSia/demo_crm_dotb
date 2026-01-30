from fastapi import FastAPI
from src.modules.users.router import router as user_router
from src.modules.crm_agent.router.router import router as agent_router

app = FastAPI(
    title="CRM API",
    description="API for CRM system with user data management",
    version="1.0.0"
)
# TODO: Add api versioning by using a global api folder with v1, v2, ect and using the individual routers from the modules

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
