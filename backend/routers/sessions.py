import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.database import get_db
from backend.db.queries import SessionQueries
from backend.models.schemas import (
    APIResponse, SessionStartRequest, SessionEndRequest,
    SessionEndResponse, SessionResponse,
)
from backend.llm_engine.client import llm_engine
from backend.config import settings

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/start", response_model=APIResponse)
async def start_session(req: SessionStartRequest, db: AsyncSession = Depends(get_db)):
    #Run LLM inference in a thread executor to avoid blocking the event loop
    loop = asyncio.get_running_loop()
    schedule = await asyncio.wait_for(
        loop.run_in_executor(
            None,
            llm_engine.generate_schedule,
            req.intent,
            req.duration_minutes,
        ),
        timeout=settings.llm_timeout_seconds,
    )

    session = await SessionQueries.create_session(
        db,
        intent=req.intent,
        schedule=schedule.model_dump_json(),
        duration_sec=schedule.total_duration_sec,
    )

    return APIResponse(
        success=True,
        message="Session started",
        data={
            "session_id": session.id,
            "schedule": schedule.model_dump(),
        },
    )


@router.patch("/{session_id}/end", response_model=SessionEndResponse)
async def end_session(
    session_id: int,
    req: SessionEndRequest,
    db: AsyncSession = Depends(get_db),
):
    session = await SessionQueries.end_session(
        db,
        session_id=session_id,
        rating=req.rating,
        feedback_note=req.feedback_note,
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return SessionEndResponse(
        session_id=session.id,
        duration_sec=session.duration_sec or 0,
    )


@router.get("/history", response_model=APIResponse)
async def session_history(
    user_id: int,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    sessions = await SessionQueries.list_by_user(db, user_id=user_id, limit=limit, offset=offset)
    return APIResponse(
        success=True,
        message="Session history",
        data={
            "sessions": [SessionResponse.model_validate(s).model_dump(mode="json") for s in sessions],
            "limit": limit,
            "offset": offset,
        },
    )


@router.websocket("/ws/{session_id}")
async def session_websocket(websocket: WebSocket, session_id: int):
    #Basic WebSocket, poc for transport. Sends connected message + ping/pong.
    await websocket.accept()
    try:
        await websocket.send_json({"type": "connected", "session_id": session_id})

        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)

            if msg.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            elif msg.get("type") == "request_schedule":
                await websocket.send_json({
                    "type": "schedule_ack",
                    "message": "Schedule delivery via WebSocket confirmed",
                })
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")
