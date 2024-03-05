from fastapi import FastAPI

from src.routers.kb_router import kb_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from graph_vault"}


app.include_router(kb_router)
