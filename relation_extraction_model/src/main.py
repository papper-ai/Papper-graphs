from typing import Annotated
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse

from src.utils.relation_extraction import run_relation_extraction

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from seq2seq"}


@app.post("/extract_relations", status_code=status.HTTP_200_OK)
def extract_relations(text: Annotated[str, Body()]) -> JSONResponse:
    relations = run_relation_extraction(text)

    return relations
