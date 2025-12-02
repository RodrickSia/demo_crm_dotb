from fastapi import FastAPI
from api.routes.user_routes import router as user_router

app = FastAPI(
    title="CRM API",
    description="API for CRM system with user data management",
    version="1.0.0"
)

app.include_router(user_router)

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
