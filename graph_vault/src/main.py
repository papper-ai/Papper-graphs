from fastapi import FastAPI

from routers.upload import upload_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from graph_vault"}


app.include_router(upload_router)
