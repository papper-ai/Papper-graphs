from fastapi import FastAPI

from src.qa_router.router import qa_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from graph_rag_service"}


app.include_router(qa_router)
