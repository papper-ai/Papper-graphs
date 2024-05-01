from fastapi import FastAPI

from model_router.router import router as model_router

app = FastAPI()
app.include_router(model_router)


@app.get("/")
def read_root():
    return {"Message": "Hello to the Embedding Model Service"}
