#queries for auth/session management and audio ops
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime, timedelta
from .database import User, AudioTrack

#CRUD ops for User
class UserQueries:
    @staticmethod
    async def create_user(
        db: AsyncSession,
        email: str,
        username: str,
        hashed_password: str,
        neurotype: Optional[str] = None,
        volume_preference: Optional[float] = 0.5
    ) -> User:
        #new user
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            neurotype=neurotype,
            user_preferences=None,
            created_at=datetime.utcnow(),
            last_active=datetime.utcnow(),
            activity=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    #User Details
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def list_users(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        result = await db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def update_last_active(db: AsyncSession, user_id: int) -> Optional[User]:
        user = await UserQueries.get_by_id(db, user_id)
        if user:
            user.last_active = datetime.utcnow()
            await db.commit()
            await db.refresh(user)
        return user


#CRUD ops for AudioTrack
class AudioTrackQueries:
    @staticmethod
    async def create_track(
        db: AsyncSession,
        name: str,
        file_path: str,
        audio_type: str,
        duration: float,
        frequency: float,
        bpm: Optional[float] = None,
        tags: Optional[str] = None
    ) -> AudioTrack:
        #new audio track
        track = AudioTrack(
            name=name,
            file_path=file_path,
            audio_type=audio_type,
            duration=duration,
            frequency=frequency,
            bpm=bpm,
            tags=tags,
            created_at=datetime.utcnow(),
            activity=True
        )
        db.add(track)
        await db.commit()
        await db.refresh(track)
        return track
    
    #Audio Track Details
    @staticmethod
    async def get_by_id(db: AsyncSession, track_id: int) -> Optional[AudioTrack]:
        result = await db.execute(
            select(AudioTrack).where(AudioTrack.id == track_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> Optional[AudioTrack]:
        result = await db.execute(
            select(AudioTrack).where(AudioTrack.name == name)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def list_tracks(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        audio_type: Optional[str] = None
    ) -> List[AudioTrack]:
        #all tracks with optional audio type
        query = select(AudioTrack)
        
        if audio_type:
            query = query.where(AudioTrack.audio_type == audio_type)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def list_by_audio_type(
        db: AsyncSession,
        audio_type: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[AudioTrack]:
        #tracks filtered by audio type
        result = await db.execute(
            select(AudioTrack)
            .where(AudioTrack.audio_type == audio_type)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all() 