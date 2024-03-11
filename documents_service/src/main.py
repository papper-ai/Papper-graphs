from fastapi import FastAPI

from src.documents.router import documents_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from documents_service"}


app.include_router(documents_router)
