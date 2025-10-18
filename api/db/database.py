from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from datetime import datetime
from typing import AsyncGenerator

from api.config import settings

#async database engine and session maker
engine = create_async_engine(settings.database_url, echo=settings.debug)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    #user neurodiversity trackers
    neurotype = Column(String, nullable=True)
    user_preferences = Column(Text, nullable=True)

    #timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    activity = Column(Boolean, nullable=True)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, neurotype={self.neurotype})>"

#Audio Track Model
class AudioTrack(Base):
    __tablename__ = "audio"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    audio_type = Column(String, nullable=False)

    #audio properties
    duration = Column(Float, nullable=False)
    frequency = Column(Float, nullable=False)
    bpm = Column(Float, nullable=True)

    #Metadata for track categories
    tags = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    activity = Column(Boolean, nullable=True)

    def __repr__(self):
        return f"<AudioTrack(name={self.name}, type={self.audio_type}, duration={self.duration}s)>"

#database dependency session management
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session: 
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
        finally:
            await session.close()

#initializing the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("DB initialized")

