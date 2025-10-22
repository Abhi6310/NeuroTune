# NeuroTune
**NeuroTune** is a personalized meditation and focus app that adapts music in real-time using audio modulation techniques catered to neurodivergent users.

------
## Features

- **Real-Time Adaptive Music Engine** 
  Binaural beats, ambient loops, and isochronic tones that evolve live during sessions.

- **Personalized Focus Recommendations** 
  Lightweight machine learning suggests sessions based on your feedback and neurotype.

- **Neurodiversity-Centered Design** 
  Minimal, predictable, sensory-friendly interface. Toggle sound layers and visuals.

- **Feedback Loop for Improvement** 
  Rate sessions and fine-tune your own audio experience over time.

------
# Scientific Backing
**NeuroTune** uses research-backed techniques shown to assist with:
- ADHD and executive functioning support
- Cognitive fatigue reduction
- Sleep and relaxation modulation via brainwave entrainment

------
# Tech Stack 
### **Frontend**
- `Flutter` – UI and Audio Engine

### **Backend**
- `FastAPI` – Python async server
- `PostgreSQL` – User/session/feedback DB

### **Machine Learning**
- `Pandas`, `NumPy`, `TensorFlow Lite`, `scikit-learn`, `LightFM` – Recommender System

------
## Architecture 
```bash
├── [Flutter App]
│
├── Adaptive UI
├── Audio Engine
├── Feedback Collector
│
├── [FastAPI Backend]
├── Recommender System
├── Session Analytics
├── PostgreSQL + S3
```
-----
## Necessary Components
- Flutter SDK (`>=3.0.0`)
- Python 3.9+
- PostgreSQL 15+

------
## Installation
```bash
# Clone the repo
git clone https://github.com/Abhi6310/NeuroTune
cd NeuroTune

# Set-up the backend
cd api
pip install -r requirements.txt
uvicorn main:app --reload

# Set-up Flutter app
cd ../app
flutter pub get
flutter run
```
-----
# Project Structure
```bash
NeuroTune/
│
├── README.md
├──.gitignore
├── requirements.txt    #For backend dependencies
├── pubspec.yaml        #Flutter app setup
│
├── /app
│   ├── /lib
│   │   ├── main.dart
│   │   ├── /screens
│   │   ├── /widgets
│   │   ├── /models
│   │   ├── /services   #API and Auth
│   │   ├── /audio      #Audio Playback
│   ├── /assets
│   │   ├── /images
│   │   ├── /sounds
│   └── test/
│
├── /api                #FastAPI backend
│   ├── main.py
│   ├── config.py
│   ├── /routes
│   │   ├── auth.py
│   │   ├── sessions.py
│   │   └── feedback.py
│   ├── /models                 #Pydantic schemas and DB models
│   ├── /ml
│   │   ├── recommender.py
│   │   └── utils.py
│   ├── /db
│   │   ├── database.py
│   │   └── queries.py
│   └── /tests
│
├── /ml                         #Data science experiments
│   ├── training.ipynb
│   ├── data_preprocessing.py
│   ├── user_clustering.py
│   └── /models
│       └── recommender_model.pkl
│
├── /audio                      #Loop layers and generative audio samples
│   ├── /sample_loops
│   └── /raw_assets             #WAV/FLAC master files
│
├── /docs                       #Documentation and UI mockups
│   ├── architecture.md
│   ├── ui_wireframes.pdf
│   ├── scientific_basis.md
│   └── tech_stack_overview.md
│
└── /scripts                    #Deployment, setup, and data scripts
    ├── deploy_backend.sh
    ├── generate_dummy_data.py
    └── setup_db.py
```
-----