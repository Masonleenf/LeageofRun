# RunBattle - Complete Development Specification for Claude Code

## Project Overview
RunBattle is a lightweight social running competition app that integrates with existing running apps (Strava, Nike Run Club) while providing its own GPS tracking using Google Maps API. The app focuses on competitive features: 1v1 battles, leagues, crew battles, and virtual marathons.

## Tech Stack
- **Frontend**: Flutter 3.22+ (iOS & Android)
- **Backend**: Python 3.10+ with FastAPI
- **Database**: PostgreSQL + Redis
- **Maps**: Google Maps API
- **Authentication**: JWT + OAuth 2.0
- **Push Notifications**: Firebase Cloud Messaging

## Project Structure
```
runbattle/
├── frontend/                 # Flutter mobile app
│   ├── lib/
│   │   ├── main.dart
│   │   ├── core/
│   │   │   ├── constants/
│   │   │   ├── themes/
│   │   │   └── utils/
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   │   ├── data/
│   │   │   │   ├── domain/
│   │   │   │   └── presentation/
│   │   │   ├── running/
│   │   │   │   ├── data/
│   │   │   │   ├── domain/
│   │   │   │   └── presentation/
│   │   │   ├── battle/
│   │   │   │   ├── data/
│   │   │   │   ├── domain/
│   │   │   │   └── presentation/
│   │   │   ├── crew/
│   │   │   └── profile/
│   │   └── shared/
│   │       ├── widgets/
│   │       └── services/
│   ├── pubspec.yaml
│   └── README.md
│
├── backend/                  # Python FastAPI server
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── runs.py
│   │   │   │   │   ├── battles.py
│   │   │   │   │   ├── leagues.py
│   │   │   │   │   ├── crews.py
│   │   │   │   │   └── integrations.py
│   │   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── run.py
│   │   │   ├── battle.py
│   │   │   ├── crew.py
│   │   │   └── league.py
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── gps_calculator.py
│   │   │   ├── matchmaking.py
│   │   │   ├── ranking.py
│   │   │   └── strava_client.py
│   │   └── utils/
│   ├── alembic/              # Database migrations
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
└── docs/                     # Documentation
    ├── API.md
    └── DEPLOYMENT.md
```

## Detailed Feature Specifications

### 1. GPS Running Tracker (Core Feature)

#### Frontend Implementation (Flutter)
**File: `frontend/lib/features/running/data/services/gps_service.dart`**

Requirements:
- Use `geolocator` package for GPS tracking
- Use `google_maps_flutter` for map display
- Implement background location tracking
- Calculate distance using Haversine formula
- Track: distance, duration, pace, speed, route points
- Update UI every 1 second
- Handle pause/resume/stop states
- Save route as polyline coordinates
- Request location permissions properly

**File: `frontend/lib/features/running/presentation/screens/running_screen.dart`**

UI Requirements:
- Top card showing: elapsed time, distance, current pace, current speed
- Google Map with:
  - User's current location marker
  - Blue polyline showing running route
  - Follow user location automatically
- Bottom control buttons:
  - Start button (green, circular)
  - Pause button (orange, circular)
  - Resume button (green, circular)
  - Stop button (red, circular)
- Show end-of-run summary dialog with statistics

#### Backend Implementation (Python)
**File: `backend/app/services/gps_calculator.py`**

Requirements:
- Implement Haversine distance calculation
- Calculate total distance from route points
- Calculate average pace (min/km)
- Calculate average speed (km/h)
- Calculate calories burned based on weight
- Analyze run segments (fastest/slowest)
- Validate GPS data quality

**File: `backend/app/api/v1/endpoints/runs.py`**

Endpoints:
```python
POST /api/v1/runs/start
  - Create new run session
  - Return run_id

POST /api/v1/runs/{run_id}/update
  - Update run progress (for live tracking)
  - Accept: latitude, longitude, timestamp

POST /api/v1/runs/{run_id}/complete
  - Finalize run
  - Calculate final statistics
  - Save to database

GET /api/v1/runs/user/{user_id}
  - Get user's run history
  - Support pagination
  - Filter by date range

GET /api/v1/runs/{run_id}
  - Get specific run details
  - Include route polyline
```

### 2. Authentication System

#### Frontend Implementation
**File: `frontend/lib/features/auth/presentation/screens/login_screen.dart`**

Requirements:
- Email/password login
- Google Sign-In integration
- Apple Sign-In integration (iOS)
- JWT token storage using `flutter_secure_storage`
- Auto-login if token valid
- Forgot password flow

**File: `frontend/lib/features/auth/data/services/auth_service.dart`**

Requirements:
- API client for auth endpoints
- Token refresh logic
- Secure token storage
- Auto logout on token expiration

#### Backend Implementation
**File: `backend/app/api/v1/endpoints/auth.py`**

Endpoints:
```python
POST /api/v1/auth/register
  - Email, password, username
  - Hash password with bcrypt
  - Return JWT token

POST /api/v1/auth/login
  - Email, password
  - Validate credentials
  - Return JWT token + refresh token

POST /api/v1/auth/refresh
  - Refresh expired token
  - Return new JWT token

POST /api/v1/auth/google
  - Google OAuth integration
  - Verify Google token
  - Create/login user

GET /api/v1/auth/me
  - Get current user info
  - Require valid JWT
```

**File: `backend/app/core/security.py`**

Requirements:
- JWT token generation with `python-jose`
- Password hashing with `bcrypt`
- Token expiration: 24 hours
- Refresh token expiration: 7 days

### 3. 1v1 Battle System

#### Frontend Implementation
**File: `frontend/lib/features/battle/presentation/screens/battle_matchmaking_screen.dart`**

Requirements:
- Show "Finding Opponent" animation
- Display matched opponent info
- Accept/decline battle
- Show battle countdown (3-2-1-GO!)
- Navigate to battle running screen

**File: `frontend/lib/features/battle/presentation/screens/battle_running_screen.dart`**

Requirements:
- Split-screen view:
  - Top half: Your stats
  - Bottom half: Opponent stats (real-time)
- Show who's winning (color indicator)
- Real-time updates using WebSocket or polling
- End battle when both complete or time limit reached

#### Backend Implementation
**File: `backend/app/api/v1/endpoints/battles.py`**

Endpoints:
```python
POST /api/v1/battles/matchmaking
  - Input: user_id, distance_km, preferred_pace
  - Find opponent with similar pace (±10%)
  - Create battle session
  - Return battle_id + opponent info

POST /api/v1/battles/{battle_id}/accept
  - Accept battle invitation
  - Start battle countdown

POST /api/v1/battles/{battle_id}/start
  - Start battle tracking
  - Initialize Redis session

POST /api/v1/battles/{battle_id}/update
  - Update battle progress
  - Store in Redis for real-time updates

GET /api/v1/battles/{battle_id}/status
  - Get real-time battle status
  - Return both participants' progress

POST /api/v1/battles/{battle_id}/complete
  - Finalize battle
  - Calculate winner
  - Update ELO ratings
```

**File: `backend/app/services/matchmaking.py`**

Requirements:
- Queue system in Redis
- Match users by pace (tolerance: ±10%)
- Consider user's tier/ranking
- Timeout after 60 seconds → add AI opponent
- Implement ELO rating system

### 4. League System

#### Frontend Implementation
**File: `frontend/lib/features/league/presentation/screens/league_screen.dart`**

Requirements:
- Display user's current tier (Bronze → Diamond)
- Show weekly leaderboard
- Display tier progress bar
- Show promotion/demotion criteria
- Weekly rewards display

#### Backend Implementation
**File: `backend/app/api/v1/endpoints/leagues.py`**

Endpoints:
```python
GET /api/v1/leagues/current
  - Get current week's league standings
  - User's tier and rank

GET /api/v1/leagues/tiers
  - Get all tier information
  - Promotion/demotion rules

POST /api/v1/leagues/calculate
  - Calculate weekly rankings (cron job)
  - Promote/demote users
  - Distribute rewards
```

**File: `backend/app/services/ranking.py`**

Requirements:
- Calculate league points based on:
  - Battle wins (points vary by opponent tier)
  - Total distance run
  - Average pace improvement
- Tier system:
  - Bronze: 0-1000 points
  - Silver: 1001-2000 points
  - Gold: 2001-3500 points
  - Platinum: 3501-5000 points
  - Diamond: 5001+ points
- Weekly reset with soft reset (50% points retention)

### 5. Crew System

#### Frontend Implementation
**File: `frontend/lib/features/crew/presentation/screens/crew_list_screen.dart`**

Requirements:
- Browse public crews
- Search crews by name
- Join/leave crew
- Create new crew

**File: `frontend/lib/features/crew/presentation/screens/crew_detail_screen.dart`**

Requirements:
- Crew statistics
- Member list with stats
- Crew leaderboard
- Crew battles history
- Admin controls (if captain)

#### Backend Implementation
**File: `backend/app/api/v1/endpoints/crews.py`**

Endpoints:
```python
POST /api/v1/crews
  - Create new crew
  - Name, description, privacy (public/private)

GET /api/v1/crews
  - List all public crews
  - Search and filter

GET /api/v1/crews/{crew_id}
  - Get crew details
  - Member list and stats

POST /api/v1/crews/{crew_id}/join
  - Join crew

DELETE /api/v1/crews/{crew_id}/leave
  - Leave crew

POST /api/v1/crews/{crew_id}/battles
  - Challenge another crew
  - Crew vs Crew battle

GET /api/v1/crews/leaderboard
  - Global crew rankings
  - Based on total distance, battles won
```

### 6. Strava Integration

#### Backend Implementation
**File: `backend/app/api/v1/endpoints/integrations.py`**

Endpoints:
```python
GET /api/v1/integrations/strava/auth
  - Initiate Strava OAuth flow
  - Return authorization URL

POST /api/v1/integrations/strava/callback
  - Handle OAuth callback
  - Exchange code for access token
  - Store tokens encrypted

GET /api/v1/integrations/strava/sync
  - Sync recent activities from Strava
  - Import as runs in RunBattle

DELETE /api/v1/integrations/strava/disconnect
  - Disconnect Strava account
```

**File: `backend/app/services/strava_client.py`**

Requirements:
- Implement Strava OAuth 2.0 flow
- API client for Strava endpoints
- Fetch activities: `/athlete/activities`
- Transform Strava activity to RunBattle run format
- Handle rate limiting (100 requests/15min)

### 7. Virtual Marathon

#### Frontend Implementation
**File: `frontend/lib/features/marathon/presentation/screens/marathon_create_screen.dart`**

Requirements:
- Form to create virtual marathon:
  - Name, distance, entry fee
  - Start/end datetime
  - Description
- Display active marathons
- Join marathon

**File: `frontend/lib/features/marathon/presentation/screens/marathon_detail_screen.dart`**

Requirements:
- Marathon details
- Participants list
- Real-time leaderboard
- Prize pool display
- Join/leave marathon

#### Backend Implementation
**File: `backend/app/api/v1/endpoints/marathons.py`**

Endpoints:
```python
POST /api/v1/marathons
  - Create virtual marathon
  - Host pays platform fee (15%)

GET /api/v1/marathons
  - List active/upcoming marathons

GET /api/v1/marathons/{marathon_id}
  - Marathon details and leaderboard

POST /api/v1/marathons/{marathon_id}/join
  - Join marathon (pay entry fee)

POST /api/v1/marathons/{marathon_id}/submit
  - Submit run for marathon
  - Validate run completed during marathon period

GET /api/v1/marathons/{marathon_id}/leaderboard
  - Real-time marathon rankings
```

### 8. Profile & Statistics

#### Frontend Implementation
**File: `frontend/lib/features/profile/presentation/screens/profile_screen.dart`**

Requirements:
- User avatar and username
- Total stats: distance, time, runs count
- Personal bests
- Achievement badges
- Recent runs list
- Settings button

**File: `frontend/lib/features/profile/presentation/screens/stats_screen.dart`**

Requirements:
- Charts using `fl_chart`:
  - Weekly distance chart
  - Monthly pace trend
  - Battle win rate
- Filterable by time period

### 9. Database Schema

**File: `backend/app/models/user.py`**
```python
class User(Base):
    id: UUID (primary key)
    email: str (unique)
    username: str (unique)
    password_hash: str
    full_name: str
    avatar_url: str
    weight_kg: float
    created_at: datetime
    
    # Stats
    total_distance_km: float
    total_duration_seconds: int
    total_runs: int
    avg_pace: float
    
    # Rankings
    elo_rating: int (default 1200)
    league_tier: str
    league_points: int
    
    # Integrations
    strava_access_token: str (encrypted)
    strava_refresh_token: str (encrypted)
    strava_athlete_id: str
```

**File: `backend/app/models/run.py`**
```python
class Run(Base):
    id: UUID (primary key)
    user_id: UUID (foreign key)
    
    # Metrics
    distance_km: float
    duration_seconds: int
    avg_pace: float
    avg_speed: float
    calories_burned: float
    
    # Route
    route_polyline: Text (encoded polyline)
    start_lat: float
    start_lng: float
    
    # Timestamps
    started_at: datetime
    completed_at: datetime
    
    # Source
    source: str ('app', 'strava', 'nike')
```

**File: `backend/app/models/battle.py`**
```python
class Battle(Base):
    id: UUID (primary key)
    
    # Participants
    user1_id: UUID (foreign key)
    user2_id: UUID (foreign key)
    
    # Battle config
    distance_km: float
    
    # Results
    winner_id: UUID (nullable)
    user1_distance: float
    user2_distance: float
    user1_time: int
    user2_time: int
    
    # Status
    status: str ('pending', 'active', 'completed')
    
    # Timestamps
    created_at: datetime
    started_at: datetime
    completed_at: datetime
```

**File: `backend/app/models/crew.py`**
```python
class Crew(Base):
    id: UUID (primary key)
    name: str (unique)
    description: str
    captain_id: UUID (foreign key)
    
    # Stats
    total_members: int
    total_distance_km: float
    battle_wins: int
    battle_losses: int
    
    # Settings
    is_public: bool
    max_members: int (default 50)
    
    created_at: datetime

class CrewMembership(Base):
    id: UUID (primary key)
    crew_id: UUID (foreign key)
    user_id: UUID (foreign key)
    role: str ('captain', 'member')
    joined_at: datetime
```

### 10. Configuration Files

**File: `frontend/pubspec.yaml`**
```yaml
name: runbattle
description: Social running competition app
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  provider: ^6.1.1
  riverpod: ^2.4.9
  
  # Network
  dio: ^5.4.0
  retrofit: ^4.0.3
  
  # Maps & Location
  google_maps_flutter: ^2.5.0
  geolocator: ^10.1.0
  geocoding: ^2.1.1
  
  # Storage
  shared_preferences: ^2.2.2
  flutter_secure_storage: ^9.0.0
  sqflite: ^2.3.0
  
  # UI
  fl_chart: ^0.65.0
  cached_network_image: ^3.3.1
  shimmer: ^3.0.0
  
  # Auth
  google_sign_in: ^6.1.5
  sign_in_with_apple: ^5.0.0
  
  # Utils
  intl: ^0.18.1
  uuid: ^4.3.3
  permission_handler: ^11.2.0
  
  # Firebase
  firebase_core: ^2.24.2
  firebase_messaging: ^14.7.9
  firebase_analytics: ^10.7.4
  
  # Monitoring
  sentry_flutter: ^7.14.0
```

**File: `backend/requirements.txt`**
```txt
# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1
redis==5.0.1

# Auth & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# HTTP Clients
httpx==0.26.0
requests==2.31.0

# Data Processing
numpy==1.26.3
pandas==2.1.4
geopy==2.4.1

# Utils
python-dateutil==2.8.2
pytz==2024.1

# Firebase
firebase-admin==6.4.0

# Monitoring
sentry-sdk==1.39.2
loguru==0.7.2

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
```

### 11. Environment Configuration

**File: `backend/app/core/config.py`**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_NAME: str = "RunBattle"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Google Maps
    GOOGLE_MAPS_API_KEY: str
    
    # Strava
    STRAVA_CLIENT_ID: str
    STRAVA_CLIENT_SECRET: str
    STRAVA_REDIRECT_URI: str
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str
    
    # Sentry
    SENTRY_DSN: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

**File: `backend/.env.example`**
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/runbattle
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here-change-in-production

# Google Maps
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# Strava Integration
STRAVA_CLIENT_ID=your-strava-client-id
STRAVA_CLIENT_SECRET=your-strava-client-secret
STRAVA_REDIRECT_URI=http://localhost:8000/api/v1/integrations/strava/callback

# Firebase
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# Sentry
SENTRY_DSN=your-sentry-dsn
```

### 12. Google Maps API Setup Instructions

**File: `docs/GOOGLE_MAPS_SETUP.md`**

Requirements:
1. Enable APIs:
   - Maps SDK for Android
   - Maps SDK for iOS
   - Geocoding API
   - Geolocation API

2. Create API Key restrictions:
   - Android: Add package name `com.runbattle.app`
   - iOS: Add bundle ID `com.runbattle.app`

3. Set billing account (required for production)

4. Configure in Android:
   - File: `android/app/src/main/AndroidManifest.xml`
   - Add meta-data tag with API key

5. Configure in iOS:
   - File: `ios/Runner/AppDelegate.swift`
   - Add GMSServices.provideAPIKey

### 13. Deployment Configuration

**File: `backend/Dockerfile`**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**File: `docker-compose.yml`**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: runbattle
      POSTGRES_USER: runbattle
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://runbattle:password@postgres:5432/runbattle
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
```

### 14. Testing Requirements

**File: `backend/tests/test_gps_calculator.py`**
Test cases:
- Haversine distance calculation accuracy
- Route total distance calculation
- Pace calculation
- Speed calculation
- Calories calculation

**File: `backend/tests/test_matchmaking.py`**
Test cases:
- Match users with similar pace
- Queue timeout handling
- ELO rating updates

**File: `backend/tests/test_auth.py`**
Test cases:
- User registration
- Login with valid/invalid credentials
- Token refresh
- JWT validation

### 15. API Documentation

**File: `docs/API.md`**

Requirements:
- Document all endpoints with:
  - Method, path
  - Request body schema
  - Response schema
  - Error codes
  - Example requests/responses
- Auto-generate using FastAPI's OpenAPI
- Available at: `/docs` (Swagger UI)

### 16. Monetization Implementation

**File: `backend/app/api/v1/endpoints/subscriptions.py`**

Endpoints:
```python
POST /api/v1/subscriptions/checkout
  - Create Stripe checkout session
  - Plans: Free, Premium ($4.99/month)

POST /api/v1/subscriptions/webhook
  - Handle Stripe webhooks
  - Update user subscription status

GET /api/v1/subscriptions/status
  - Get user's subscription status
```

Premium Features:
- Unlimited battles (free: 5/month)
- Multiple crew memberships (free: 1)
- Ad removal
- Advanced statistics
- Custom themes

### 17. Push Notifications

**File: `backend/app/services/notification_service.py`**

Notification triggers:
- Battle invitation received
- Battle starting countdown
- Battle result
- Crew invitation
- League tier promotion/demotion
- Virtual marathon starting soon
- Weekly league results

## Implementation Priority

### Phase 1 (MVP - 2 months)
1. Setup project structure
2. GPS tracking with Google Maps
3. Authentication (email/password)
4. Save/view run history
5. Basic battle system (async)
6. Simple leaderboard

### Phase 2 (Core Features - 2 months)
1. Real-time battles
2. League system
3. Crew system
4. Strava integration
5. Push notifications

### Phase 3 (Advanced - 2 months)
1. Virtual marathons
2. Premium subscription
3. Advanced analytics
4. Social features (follow, feed)
5. Achievement system

## Key Implementation Notes

1. **GPS Accuracy**: Filter out points with accuracy > 50 meters
2. **Battery Optimization**: Use distance filter (5-10 meters) instead of time intervals
3. **Offline Mode**: Queue run data locally, sync when online
4. **Real-time Updates**: Use WebSocket for battle updates (Socket.io)
5. **Caching**: Cache leaderboards in Redis (5 min TTL)
6. **Rate Limiting**: Implement per-user rate limits (100 req/min)
7. **Error Handling**: Graceful degradation when GPS unavailable
8. **Security**: 
   - Never store API keys in code
   - Encrypt sensitive data at rest
   - Use HTTPS only
   - Implement CORS properly

## Development Commands

### Frontend (Flutter)
```bash
# Get dependencies
flutter pub get

# Run on device
flutter run

# Build APK
flutter build apk --release

# Build iOS
flutter build ios --release

# Run tests
flutter test
```

### Backend (Python)
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

# Run migrations
alembic upgrade head

# Create migration
alembic revision --autogenerate -m "description"

# Run tests
pytest

# Run with Docker
docker-compose up
```

## Success Metrics

Track these KPIs:
- Daily Active Users (DAU)
- Average session duration
- Battles per user per week
- Crew participation rate
- Strava integration rate
- Premium conversion rate
- User retention (D1, D7, D30)

## Support & Resources

- Flutter: https://flutter.dev/docs
- FastAPI: https://fastapi.tiangolo.com
- Google Maps Platform: https://developers.google.com/maps
- Strava API: https://developers.strava.com
- PostgreSQL: https://www.postgresql.org/docs
- Redis: https://redis.io/docs

---

## IMPORTANT: Instructions for Claude Code

When implementing this project:

1. **Start with Phase 1 MVP** - Don't try to build everything at once
2. **Follow the exact file structure** specified above
3. **Implement features in order** of priority
4. **Write clean, documented code** with proper error handling
5. **Test each feature** before moving to the next
6. **Use environment variables** for all secrets
7. **Follow best practices** for Flutter (BLoC/Provider) and FastAPI
8. **Implement proper logging** using loguru (Python) and flutter logging
9. **Add comprehensive comments** explaining complex logic
10. **Create README files** in each major directory

This specification is complete and ready for implementation. Each file path and endpoint is clearly defined. Follow the structure exactly and implement features incrementally.
