import numpy as np
from typing import Optional

PITCH_CLASSES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def analyze_track(file_path: str) -> dict:
    #Extract BPM, key signature, and duration using librosa
    #Returns dict with nullable fields so track still gets cataloged on failure
    import librosa

    try:
        y, sr = librosa.load(file_path, sr=22050)
    except Exception:
        return {"duration_sec": None, "bpm": None, "key_signature": None}

    #Duration
    duration_sec = float(librosa.get_duration(y=y, sr=sr))

    #BPM via beat tracking
    bpm = _extract_bpm(y, sr)

    #Key via chroma analysis
    key_signature = _extract_key(y, sr)

    return {
        "duration_sec": duration_sec,
        "bpm": bpm,
        "key_signature": key_signature,
    }


def _extract_bpm(y: np.ndarray, sr: int) -> Optional[float]:
    try:
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        # librosa >= 0.10 returns an array
        if hasattr(tempo, "__len__"):
            return float(tempo[0])
        return float(tempo)
    except Exception:
        return None


def _extract_key(y: np.ndarray, sr: int) -> Optional[str]:
    try:
        import librosa
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        key_index = int(np.argmax(chroma_mean))
        return PITCH_CLASSES[key_index]
    except Exception:
        return None
