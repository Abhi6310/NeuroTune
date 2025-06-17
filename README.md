# NeuroTune
**NeuroTune** is a personalized meditation and focus app that adapts music in real-time using audio modulation techniques catered to neurodivergent users.

------
## Features 🚀

- **Real-Time Adaptive Music Engine** 🎶
  Binaural beats, ambient loops, and isochronic tones that evolve live during sessions.

- **Personalized Focus Recommendations** 🧠
  Lightweight machine learning suggests sessions based on your feedback and neurotype.

- **Neurodiversity-Centered Design** 🧘
  Minimal, predictable, sensory-friendly interface. Toggle sound layers and visuals.

- **Feedback Loop for Improvement** 📊
  Rate sessions and fine-tune your own audio experience over time.

------
# Science 🧪
**NeuroTune** uses research-backed techniques shown to assist with:
- ADHD and executive functioning support
- Cognitive fatigue reduction
- Sleep and relaxation modulation via brainwave entrainment

Sources:  
- [Frontiers in Human Neuroscience](https://www.frontiersin.org/journals/human-neuroscience)  
- [Clinical EEG and Neuroscience](https://journals.sagepub.com/home/eeg)

------
# Tech Stack 🛠️
### **Frontend**
- `Flutter` – Cross-platform UI
- `Flutter_sound` / `Superpowered SDK` – Low-latency audio engine
- `Riverpod` – State management

### **Backend**
- `FastAPI` – Python async server
- `PostgreSQL` – User/session/feedback DB
- `AWS S3` – Audio file storage
- `Firebase Auth` – Secure authentication

### **Machine Learning**
- `LightFM` – Hybrid recommender system
- `scikit-learn` – Feedback clustering
- `TensorFlow Lite` – On-device inference
- `Pandas`, `NumPy` – Data processing

------
## Architecture 🧱
[Flutter App]
├──Adaptive UI
├──Audio Engine
├──Feedback Collector
|
[FastAPI Backend]
├──Recommender System
├──Session Analytics
├──PostgreSQL + S3

-----
## Necessary Components 🔧
- Flutter SDK (`>=3.0.0`)
- Python 3.9+
- PostgreSQL 15+
- AWS S3 or local storage setup
- Firebase Auth project (optional)

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
## Demo Audio
Sample layered soundscapes will be implemented soon. Note: sample music will be non-copyright for non-commercial use

-----
## Acknowledgements
Inspired by Brain.fm and Calm, built with neurodivergence in mind

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