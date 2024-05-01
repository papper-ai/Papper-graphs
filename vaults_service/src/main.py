from fastapi import FastAPI

from src.vaults.router import vaults_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from vaults_service"}


app.include_router(vaults_router)
