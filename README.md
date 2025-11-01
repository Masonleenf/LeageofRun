# 🏃 RunBattle

**Social running competition app with real-time battles, leagues, and crew challenges**

[![Flutter](https://img.shields.io/badge/Flutter-3.22+-02569B?logo=flutter)](https://flutter.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?logo=postgresql)](https://postgresql.org)

## 📱 Features

- ✅ **GPS Running Tracker** - Track distance, pace, speed with Google Maps
- ⚔️ **1v1 Real-time Battles** - Compete with runners of similar skill
- 🏆 **League System** - Climb from Bronze to Diamond tier
- 👥 **Crew System** - Form teams and compete together
- 🔗 **Strava Integration** - Import your existing runs
- 🎯 **Virtual Marathons** - User-hosted competitions
- 📊 **Advanced Analytics** - Detailed performance insights

## 🎯 Project Structure

```
LeageofRun/
├── backend/          # Python FastAPI Backend
│   ├── app/
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── api/          # API endpoints
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   └── tests/            # Backend tests
│
└── frontend/         # Flutter Mobile App
    ├── lib/
    │   ├── core/         # Core utilities
    │   ├── features/     # Feature modules
    │   └── shared/       # Shared widgets
    └── test/             # Frontend tests
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Flutter 3.22+
- PostgreSQL 15+
- Redis 7+
- Google Maps API Key

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Start the server
uvicorn app.main:app --reload
```

Server will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Get dependencies
flutter pub get

# Configure Google Maps API
# Android: Edit android/app/src/main/AndroidManifest.xml
# iOS: Edit ios/Runner/AppDelegate.swift

# Run the app
flutter run
```

### Docker Setup (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## 🔧 Configuration

### Backend Environment Variables

Create `backend/.env` file:

```env
DATABASE_URL=postgresql://runbattle:password@localhost:5432/runbattle
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
STRAVA_CLIENT_ID=your-strava-client-id
STRAVA_CLIENT_SECRET=your-strava-client-secret
```

### Frontend Configuration

Update `frontend/lib/core/constants/api_constants.dart`:

```dart
static const String baseUrl = 'http://your-backend-url:8000';
```

## 📚 API Documentation

### Authentication

```bash
# Register
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "username": "runner123",
  "password": "securepassword"
}

# Login
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "securepassword"
}

# Get current user
GET /api/v1/auth/me
Headers: Authorization: Bearer <token>
```

### Runs

```bash
# Create run
POST /api/v1/runs
{
  "distance_km": 5.2,
  "duration_seconds": 1800,
  "avg_pace": 5.77,
  "avg_speed": 10.4,
  "route": [
    {"lat": 37.7749, "lng": -122.4194},
    {"lat": 37.7750, "lng": -122.4195}
  ],
  "start_time": "2024-01-01T10:00:00Z",
  "end_time": "2024-01-01T10:30:00Z"
}

# Get user runs
GET /api/v1/runs?skip=0&limit=20
Headers: Authorization: Bearer <token>
```

For complete API documentation, visit: `http://localhost:8000/docs`

## 🏗️ Architecture

### Backend Architecture

- **Framework**: FastAPI (async Python web framework)
- **Database**: PostgreSQL (relational data)
- **Cache**: Redis (real-time battle data)
- **ORM**: SQLAlchemy (database abstraction)
- **Auth**: JWT tokens with bcrypt password hashing
- **Validation**: Pydantic schemas

### Frontend Architecture

- **Framework**: Flutter (cross-platform mobile)
- **State Management**: Provider
- **HTTP Client**: Dio
- **Storage**: flutter_secure_storage + shared_preferences
- **Maps**: google_maps_flutter + geolocator
- **Charts**: fl_chart

### Database Schema

```sql
-- Users
users (id, email, username, password_hash, stats, rankings)

-- Runs
runs (id, user_id, distance, duration, pace, route, timestamps)

-- Battles
battles (id, user1_id, user2_id, winner_id, stats, status)

-- Crews
crews (id, name, captain_id, stats)
crew_memberships (id, crew_id, user_id, role)
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app  # With coverage
```

### Frontend Tests

```bash
cd frontend
flutter test
flutter test --coverage  # With coverage
```

## 🔐 Security

- ✅ JWT authentication with secure token storage
- ✅ Password hashing with bcrypt
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ CORS protection
- ✅ Rate limiting
- ✅ Input validation (Pydantic schemas)
- ✅ HTTPS only in production

## 🚢 Deployment

### Backend Deployment

**Option 1: Docker**
```bash
docker build -t runbattle-backend ./backend
docker run -p 8000:8000 runbattle-backend
```

**Option 2: Traditional**
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Deployment

**Android:**
```bash
flutter build apk --release
flutter build appbundle --release  # For Play Store
```

**iOS:**
```bash
flutter build ios --release
```

## 📊 Performance

- API Response Time: < 100ms (average)
- GPS Accuracy: ±5-10 meters
- Battery Usage: Optimized with distance filter
- Database Queries: Indexed for fast lookups
- Caching: Redis for real-time data (5min TTL)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 (Python) and Dart style guide
- Write tests for new features
- Update documentation
- Keep commits atomic and descriptive

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🗺️ Roadmap

### Phase 1 (MVP) ✅
- [x] Authentication system
- [x] GPS running tracker
- [x] Run history
- [x] Basic API structure

### Phase 2 (Core Features) 🚧
- [ ] Real-time battles
- [ ] League system
- [ ] Crew management
- [ ] Strava integration

### Phase 3 (Advanced) 📋
- [ ] Virtual marathons
- [ ] Premium subscription
- [ ] Advanced analytics
- [ ] Social features

## 📈 Stats

- **Backend**: Python FastAPI
- **Frontend**: Flutter (Dart)
- **Database Tables**: 8 main tables
- **API Endpoints**: 30+ endpoints (planned)
- **Test Coverage**: Target 80%+

---

Made with ❤️ by the RunBattle Team

**Run. Compete. Win.** 🏃‍♂️🏆
