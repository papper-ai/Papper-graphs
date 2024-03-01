from fastapi import FastAPI

from src.utils.relation_extraction import run_relation_extraction

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from seq2seq"}


@app.post("/extract_relations")
def extract_relations(input: str):
    relations = run_relation_extraction(input)

    return relations
