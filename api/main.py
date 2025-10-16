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

#App instance
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan
)

#CORS Middleware
#api runs on localhost:8000, frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

#GET
@app.get("/", response_model=APIResponse)
async def root():
    return APIResponse(
        success=True,
        message="API running",
        data={
            "version": settings.api_version,
            "description": settings.api_description
        }
    )

@app.get("/health", response_model=APIResponse)
async def health_check():
    """Health check endpoint"""
    return APIResponse(
        success=True,
        message="API health check",
        data={
            "status": "healthy",
            "version": settings.api_version
        }
    )

#Error Handling
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint error",
            "details": f"Endpoint {request.url.path} doesn't exist"
        }
    )


@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "details": "Server errored"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )