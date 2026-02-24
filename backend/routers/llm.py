import asyncio
from fastapi import APIRouter, HTTPException

from backend.models.schemas import GenerateScheduleRequest, APIResponse
from backend.llm_engine.client import llm_engine
from backend.config import settings

router = APIRouter(prefix="/llm", tags=["llm"])


@router.post("/generate-schedule", response_model=APIResponse)
async def generate_schedule(req: GenerateScheduleRequest):
    #Standalone schedule generation, decoupled from session creation
    try:
        loop = asyncio.get_running_loop()
        schedule = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                llm_engine.generate_schedule,
                req.intent,
                req.duration_min,
            ),
            timeout=settings.llm_timeout_seconds,
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="LLM inference timed out")

    return APIResponse(
        success=True,
        message="Schedule generated",
        data={"schedule": schedule.model_dump()},
    )
