from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, func


class Base(DeclarativeBase):
    pass

#User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    #user neurodiversity trackers
    neurotype = Column(String(50), nullable=True)
    user_preferences = Column(Text, nullable=True)

    #timestamps
    created_at = Column(DateTime, server_default=func.now())
    last_active = Column(DateTime, server_default=func.now())
    activity = Column(Boolean, nullable=True)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, neurotype={self.neurotype})>"

#Audio Track model
class AudioTrack(Base):
    __tablename__ = "audio"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    audio_type = Column(String(50), nullable=False)

    #audio properties
    duration = Column(Float, nullable=False)
    frequency = Column(Float, nullable=False)
    bpm = Column(Float, nullable=True)

    #Metadata for track categories
    tags = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    activity = Column(Boolean, nullable=True)

    def __repr__(self):
        return f"<AudioTrack(name={self.name}, type={self.audio_type}, duration={self.duration}s)>"

#Session model — tracks LLM-generated audio sessions
class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # nullable for MVP (no auth)
    intent = Column(String(100), nullable=False)
    schedule = Column(Text, nullable=False)  # JSON string
    duration_sec = Column(Integer, nullable=True)
    started_at = Column(DateTime, server_default=func.now())
    ended_at = Column(DateTime, nullable=True)
    rating = Column(Integer, nullable=True)
    feedback_note = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Session(intent={self.intent}, duration={self.duration_sec}s)>"
