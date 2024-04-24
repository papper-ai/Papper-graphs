from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.kb_router.router import kb_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"message": "Hello from graph_kb_service"}

app.include_router(kb_router)
