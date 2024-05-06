from fastapi import FastAPI
from qa_router.router import router as qa_router


app = FastAPI()
app.include_router(qa_router, prefix="/qa")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8002)

