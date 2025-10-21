#Database Setup and Initialization
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from api.db.database import init_db, async_session_factory
from api.db.queries import UserQueries, AudioTrackQueries

async def demo_users(session):
    demo_users = [
        {
            "email": "demo@neurotune.com",
            "username": "demo_adhd",
            "hashed_password": "demo_hashed_password_adhd",
            "neurotype": "ADHD",
        },
        {
            "email": "demo2@neurotune.com",
            "username": "demo2_neurotypical",
            "hashed_password": "demo2_hashed_password_neurotypical",
            "neurotype": "Neurotypical",
        }]
    created_count = 0
    for user_data in demo_users:
        #if user already exists, skip, otherwise make user
        existing = await UserQueries.get_by_email(session, user_data["email"])
        if not existing:
            await UserQueries.create_user(
                db=session,
                email=user_data["email"],
                username=user_data["username"],
                hashed_password=user_data["hashed_password"],
                neurotype=user_data["neurotype"],
                volume_preference=0.5
            )
            created_count += 1
            print(f"Created user: {user_data['username']}")
        else:
            print(f"User already exists: {user_data['username']}")
    return created_count

#demo audio tracks
async def demo_audio(session):
    demo_tracks = [
        #10Hz Alpha binaural
        {
            "name": "Focus Flow - Alpha Waves",
            "file_path": "/audio/focus_alpha_10hz.mp3",
            "audio_type": "binaural",
            "duration": 600.0,
            "frequency": 10.0, 
            "bpm": 60.0,
            "tags": "focus,concentration,study,alpha"
        },
        {
            #6Hz Theta isochronic
            "name": "Deep Relaxation - Theta",
            "file_path": "/audio/relax_theta_6hz.mp3",
            "audio_type": "isochronic",
            "duration": 1200.0,
            "frequency": 6.0, 
            "bpm": 45.0,
            "tags": "relaxation,meditation,anxiety-relief,theta"
        },
        {
            #Nature sounds
            "name": "Calm Waters - Nature Sounds",
            "file_path": "/audio/nature_water.mp3",
            "audio_type": "nature",
            "duration": 900.0,
            "frequency": 0.0,
            "bpm": None,
            "tags": "nature,calm,background,water"
        }]
    
    created_count = 0
    for track_data in demo_tracks:
        #if track already exists, skip, otherwise make track
        existing = await AudioTrackQueries.get_by_name(session, track_data["name"])
        if not existing:
            await AudioTrackQueries.create_track(
                db=session,
                name=track_data["name"],
                file_path=track_data["file_path"],
                audio_type=track_data["audio_type"],
                duration=track_data["duration"],
                frequency=track_data["frequency"],
                bpm=track_data["bpm"],
                tags=track_data["tags"]
            )
            created_count += 1
            print(f"Created track: {track_data['name']}")
        else:
            print(f"Track already exists: {track_data['name']}")
    
    return created_count


async def main():
    print("NeuroTune Database Setup")
    #Initializing db
    try:
        await init_db()
        print("\nDb tables working")
    except Exception as e:
        print(f"\nError initializing database: {e}")
        return
    
    #Demo data
    async with async_session_factory() as session:
        try:
            users_created = await demo_users(session)
            tracks_created = await demo_audio(session)
            await session.commit()
            #Summary
            print("\n Summary")
            print("=" * 60)
            print(f"Users created: {users_created}")
            print(f"Audio tracks created: {tracks_created}")
            print(f"Total records created: {users_created + tracks_created}")
            print("=" * 60)
            print("\n Database setup complete")
            
        except Exception as e:
            print(f"\nDemo data error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(main())
