from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from api.models.schemas import APIResponse
from api.config import settings
from api.database import APIResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Neurotune starting up (API)")
    try:
        await init_db()
        print("Initialized Database")
    except Exception as e:
        print(f"DB Setup Error: {e}")
    yield
    print ("API shutting down")

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

