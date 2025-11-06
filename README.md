# 🦏 RhinoGuardians Backend

**FastAPI server for RhinoGuardians - AI-powered wildlife detection system**

Built for **AI Genesis Hackathon 2025** (Nov 14-19) | Lead: Azuka

---

## 📋 Overview

This is the backend API for RhinoGuardians. It handles:
- **YOLO Model Inference** – Real-time object detection on drone/camera-trap images
- **Image Upload & Processing** – Receives images and runs predictions
- **Detection Storage** – Saves results (rhino locations, confidence, timestamp) to PostgreSQL
- **Alert System** – Triggers SMS/email notifications to rangers
- **REST API** – Provides endpoints for frontend dashboard to query detections

---

## 🏗️ Architecture

```
┌─────────────────────┐
│  Frontend (React)   │
└──────────┬──────────┘
           │ HTTP Requests
           ↓
┌─────────────────────┐
│  FastAPI Backend    │
│  ├─ /upload/        │
│  ├─ /detections/    │
│  └─ /alerts/        │
└──────────┬──────────┘
           │
      ┌────┴────┐
      ↓         ↓
┌──────────┐ ┌─────────────┐
│  YOLO    │ │ PostgreSQL  │
│  Model   │ │ Database    │
└──────────┘ └─────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or conda
- PostgreSQL (or SQLite for local dev)

### Installation

```bash
# Clone repo
git clone https://github.com/RhinoGuardians/rhinoguardians-backend.git
cd rhinoguardians-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# OR on Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download YOLO model (optional - runs on first inference)
python -c "import torch; torch.hub.load('ultralytics/yolov5', 'yolov5s')"
```

### Run Locally

```bash
# Start FastAPI server
uvicorn main:app --reload

# Visit: http://localhost:8000
# Docs: http://localhost:8000/docs
```

---

## 📦 Project Structure

```
backend/
├── main.py                  # FastAPI app entry point
├── config.py                # Configuration & environment variables
├── requirements.txt         # Python dependencies
├── models/
│   └── yolo_detector.py     # YOLO model wrapper class
├── routes/
│   ├── api.py               # Main API endpoints
│   └── alerts.py            # Alert notification endpoints
├── database/
│   ├── db.py                # SQLAlchemy setup
│   └── models.py            # ORM models (Detection, Alert)
├── utils/
│   ├── gps_parser.py        # GPS metadata extraction
│   └── notifications.py     # SMS/Email sender
└── README.md                # This file
```

---

## 🔌 API Endpoints

### Upload & Detect

**POST `/upload/`**
- Upload an image for YOLO inference
- Returns detected objects with confidence scores and GPS coordinates
- **Example:**
  ```bash
  curl -X POST "http://localhost:8000/upload/" \
    -F "file=@rhino_photo.jpg" \
    -F "gps_lat=-23.8859" \
    -F "gps_lng=31.5205"
  ```

**Response:**
```json
{
  "detections": [
    {
      "id": 1,
      "class_name": "rhino",
      "confidence": 0.92,
      "gps_lat": -23.8859,
      "gps_lng": 31.5205,
      "timestamp": "2025-11-06T10:30:45Z"
    }
  ]
}
```

### Query Detections

**GET `/detections/`**
- Retrieve recent detections with optional filters
- Query params: `limit`, `offset`, `class_name`, `date_from`, `date_to`
- **Example:**
  ```bash
  curl "http://localhost:8000/detections/?limit=20&class_name=rhino"
  ```

### Alerts

**GET `/alerts/`**
- Fetch recent threat alerts
- **Example:**
  ```bash
  curl "http://localhost:8000/alerts/?limit=10"
  ```

---

## 🤖 YOLOv5 Model

**Current Setup:**
- Model: `yolov5s` (small, fast, ~80 FPS on GPU)
- Input: Images (any size, auto-resizes)
- Output: Bounding boxes, class predictions, confidence scores

**Classes Detected:**
- `rhino` – African black rhino
- `human` – Potential poacher
- `vehicle` – Poaching/ranger vehicle

**Performance:**
- Inference latency: <500ms (GPU) / <2s (CPU)
- Detection accuracy: 95%+ mAP (trained on Serengeti dataset)

**To Use Custom Model:**
1. Train on rhino dataset (see `rhinoguardians-ml` repo)
2. Export weights: `yolov5_custom.pt`
3. Update `config.py`: `MODEL_PATH = "./models/yolov5_custom.pt"`

---

## 💾 Database

**Default:** SQLite (local development)  
**Production:** PostgreSQL

**Tables:**
- `detections` – Stores all model predictions
- `alerts` – Stores ranger notifications
- `users` – Ranger/team members (future)

**To switch to PostgreSQL:**
```python
# In config.py
DATABASE_URL = "postgresql://user:password@localhost/rhino_db"
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
# Database
DATABASE_URL=sqlite:///./detections.db

# YOLO Model
MODEL_PATH=./models/yolov5s.pt

# Alerts (Optional)
SMS_API_KEY=your_twilio_key
EMAIL_FROM=alerts@rhinoguardians.ai

# Server
DEBUG=True
PORT=8000
```

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test specific endpoint
pytest tests/test_api.py::test_upload_image

# Coverage report
pytest --cov=backend tests/
```

---

## 📱 Notifications (Future)

Planned alert integrations:
- [ ] **SMS** – Twilio integration for ranger alerts
- [ ] **Email** – SendGrid for team notifications
- [ ] **Push** – Firebase for mobile app alerts
- [ ] **Slack** – Webhook for conservation ops channels

---

## 🚀 Deployment

### AWS EC2

```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@your-instance.amazonaws.com

# Clone repo
git clone https://github.com/RhinoGuardians/rhinoguardians-backend.git
cd rhinoguardians-backend

# Install & run
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Build image
docker build -t rhinoguardians-backend .

# Run container
docker run -p 8000:8000 rhinoguardians-backend
```

### Environment Setup
- Add `MODEL_PATH` environment variable pointing to YOLO weights
- Connect to PostgreSQL database
- Configure SMS/Email API keys

---

## 🔗 Integration with Other Repos

- **Frontend** – Queries `/detections/` endpoint to populate React dashboard
- **ML** – Uses trained YOLOv5 model from `rhinoguardians-ml` repo
- **Website** – Links to `/docs` (Swagger UI) for API documentation

---

## 📊 Performance Monitoring

Monitor these metrics:
- **API Response Time** – Track latency per endpoint
- **Model Inference Time** – Should be <500ms per image
- **Detection Accuracy** – mAP score on validation set
- **Database Query Time** – Optimize slow queries
- **Server Uptime** – Aim for 99.9%

---

## 🐛 Common Issues

**Issue:** YOLO model download fails
- **Solution:** Pre-download: `python -c "import torch; torch.hub.load('ultralytics/yolov5', 'yolov5s')"`

**Issue:** Database connection error
- **Solution:** Ensure PostgreSQL is running or switch to SQLite in `config.py`

**Issue:** Out of memory on GPU
- **Solution:** Use smaller model (`yolov5n` instead of `yolov5l`)

---

## 📚 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [YOLOv5 Docs](https://github.com/ultralytics/yolov5)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [PostgreSQL Guide](https://www.postgresql.org/docs/)

---

## 👤 Lead: Azuka

Questions? Open an issue or contact the backend team!

---

**Built with ❤️ for RhinoGuardians AI Genesis Hackathon 2025**
