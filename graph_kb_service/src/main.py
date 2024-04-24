from fastapi import FastAPI

from src.kb_router.router import kb_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from graph_kb_service"}


app.include_router(kb_router)
