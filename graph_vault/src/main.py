from fastapi import FastAPI

from routers.upload import upload_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Bipka World"}


app.include_router(upload_router)
