import uvicorn

from kb_router.router import kb_router

from fastapi import FastAPI

app = FastAPI()
app.include_router(kb_router)

if __name__ == "__main__":
    uvicorn.run(app)