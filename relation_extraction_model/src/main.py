from fastapi import FastAPI

from src.relation_extraction import relation_extraction_router

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from relation_extraction_model"}


app.include_router(relation_extraction_router)
