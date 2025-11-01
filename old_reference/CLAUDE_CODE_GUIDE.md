# RunBattle - Claude Code Implementation Guide

## Quick Start for Claude Code

This document provides step-by-step instructions for implementing RunBattle using Claude Code.

## Prerequisites Check

Before starting, ensure you have:
- [ ] Flutter SDK 3.22+ installed
- [ ] Python 3.10+ installed
- [ ] PostgreSQL installed
- [ ] Redis installed
- [ ] Google Maps API key
- [ ] Git initialized

## Implementation Order

### 🎯 PHASE 1: Foundation (Week 1-2)

#### Step 1: Project Initialization
```bash
# Create project directory
mkdir runbattle
cd runbattle

# Initialize git
git init

# Create frontend Flutter app
flutter create frontend
cd frontend

# Create backend directory
cd ..
mkdir -p backend/app
```

#### Step 2: Setup Backend Structure
Create these files in order:

1. **`backend/requirements.txt`**
   - Copy dependencies from specification
   - Run: `pip install -r requirements.txt`

2. **`backend/app/core/config.py`**
   - Define Settings class
   - Load environment variables

3. **`backend/app/core/database.py`**
   - Setup SQLAlchemy engine
   - Create Base class
   - Create session factory

4. **`backend/app/main.py`**
   - Create FastAPI app
   - Add CORS middleware
   - Include routers
   - Health check endpoint

#### Step 3: Setup Frontend Structure
Create these files in order:

1. **`frontend/pubspec.yaml`**
   - Add all dependencies from specification
   - Run: `flutter pub get`

2. **`frontend/lib/core/constants/api_constants.dart`**
   - Define API base URL
   - Define endpoints

3. **`frontend/lib/core/utils/dio_client.dart`**
   - Setup Dio HTTP client
   - Add interceptors
   - Error handling

### 🎯 PHASE 2: Authentication (Week 3-4)

#### Backend Implementation
Create files in this order:

1. **`backend/app/models/user.py`**
   ```python
   # SQLAlchemy User model
   # Fields: id, email, username, password_hash, etc.
   ```

2. **`backend/app/schemas/user.py`**
   ```python
   # Pydantic schemas for validation
   # UserCreate, UserLogin, UserResponse
   ```

3. **`backend/app/core/security.py`**
   ```python
   # Password hashing
   # JWT token creation/validation
   # get_password_hash()
   # verify_password()
   # create_access_token()
   ```

4. **`backend/app/api/v1/endpoints/auth.py`**
   ```python
   # POST /register
   # POST /login
   # POST /refresh
   # GET /me
   ```

#### Frontend Implementation
Create files in this order:

1. **`frontend/lib/features/auth/data/models/user_model.dart`**
   ```dart
   // User model with JSON serialization
   ```

2. **`frontend/lib/features/auth/data/services/auth_service.dart`**
   ```dart
   // API calls for auth
   // register(), login(), logout()
   ```

3. **`frontend/lib/features/auth/presentation/providers/auth_provider.dart`**
   ```dart
   // State management for auth
   // Using Provider or Riverpod
   ```

4. **`frontend/lib/features/auth/presentation/screens/login_screen.dart`**
   ```dart
   // Login UI
   // Email/password fields
   // Login button
   ```

5. **`frontend/lib/features/auth/presentation/screens/register_screen.dart`**
   ```dart
   // Registration UI
   ```

### 🎯 PHASE 3: GPS Tracking (Week 5-6)

#### Backend Implementation

1. **`backend/app/services/gps_calculator.py`**
   - Implement Haversine distance formula
   - Calculate pace, speed, calories
   - Full implementation from specification

2. **`backend/app/models/run.py`**
   - SQLAlchemy Run model
   - Fields from specification

3. **`backend/app/schemas/run.py`**
   - RunCreate, RunUpdate, RunResponse schemas

4. **`backend/app/api/v1/endpoints/runs.py`**
   - POST /runs/start
   - POST /runs/{id}/update
   - POST /runs/{id}/complete
   - GET /runs/user/{user_id}

#### Frontend Implementation

1. **`frontend/lib/features/running/data/services/gps_service.dart`**
   - Use geolocator package
   - startTracking()
   - pauseTracking()
   - stopTracking()
   - Calculate distance in real-time

2. **`frontend/lib/features/running/presentation/screens/running_screen.dart`**
   - Google Maps integration
   - Stats display
   - Control buttons
   - Full implementation from specification

3. **`frontend/lib/features/running/presentation/widgets/stats_card.dart`**
   - Display distance, time, pace, speed

4. **Test GPS tracking thoroughly before proceeding**

### 🎯 PHASE 4: Battle System (Week 7-8)

#### Backend Implementation

1. **`backend/app/models/battle.py`**
   - Battle model with status tracking

2. **`backend/app/services/matchmaking.py`**
   - Queue system using Redis
   - Match by pace similarity
   - ELO rating implementation

3. **`backend/app/api/v1/endpoints/battles.py`**
   - POST /battles/matchmaking
   - POST /battles/{id}/accept
   - POST /battles/{id}/start
   - GET /battles/{id}/status
   - POST /battles/{id}/complete

4. **`backend/app/services/redis_client.py`**
   - Redis connection
   - Battle queue operations
   - Real-time status updates

#### Frontend Implementation

1. **`frontend/lib/features/battle/presentation/screens/battle_matchmaking_screen.dart`**
   - "Finding opponent" UI
   - Accept/decline battle

2. **`frontend/lib/features/battle/presentation/screens/battle_running_screen.dart`**
   - Split-screen battle UI
   - Real-time opponent tracking
   - Winner announcement

3. **`frontend/lib/features/battle/data/services/battle_service.dart`**
   - API calls
   - WebSocket/polling for real-time updates

### 🎯 PHASE 5: Social Features (Week 9-10)

#### Backend Implementation

1. **`backend/app/models/crew.py`**
   - Crew and CrewMembership models

2. **`backend/app/api/v1/endpoints/crews.py`**
   - CRUD operations for crews
   - Join/leave functionality

3. **`backend/app/api/v1/endpoints/leagues.py`**
   - League standings
   - Tier calculations

#### Frontend Implementation

1. **`frontend/lib/features/crew/presentation/screens/crew_list_screen.dart`**
   - Browse and search crews

2. **`frontend/lib/features/league/presentation/screens/league_screen.dart`**
   - Display league standings

### 🎯 PHASE 6: Integrations (Week 11-12)

#### Strava Integration

1. **`backend/app/services/strava_client.py`**
   - OAuth 2.0 flow
   - Activity sync

2. **`backend/app/api/v1/endpoints/integrations.py`**
   - Strava auth endpoints
   - Activity import

3. **`frontend/lib/features/profile/presentation/screens/integrations_screen.dart`**
   - Connect Strava button
   - OAuth flow handler

## Testing Strategy

### Unit Tests
For each feature, write tests:

**Backend:**
```python
# backend/tests/test_gps_calculator.py
def test_haversine_distance():
    # Test distance calculation accuracy
    
def test_pace_calculation():
    # Test pace formula
```

**Frontend:**
```dart
// frontend/test/gps_service_test.dart
void main() {
  test('Calculate distance correctly', () {
    // Test GPS service
  });
}
```

### Integration Tests

**Backend:**
```python
# backend/tests/test_battles.py
async def test_battle_matchmaking():
    # Test full battle flow
```

**Frontend:**
```dart
// frontend/integration_test/app_test.dart
testWidgets('Complete running session', (tester) async {
  // Test full running flow
});
```

## Database Migrations

After creating each model:

```bash
# Create migration
alembic revision --autogenerate -m "Add user model"

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

## Environment Setup

### Backend `.env` file:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/runbattle
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=generate-with-openssl-rand-hex-32
GOOGLE_MAPS_API_KEY=your-key-here
STRAVA_CLIENT_ID=your-strava-client-id
STRAVA_CLIENT_SECRET=your-strava-client-secret
```

### Frontend Configuration:

**Android:** `android/app/src/main/AndroidManifest.xml`
```xml
<meta-data
    android:name="com.google.android.geo.API_KEY"
    android:value="YOUR_GOOGLE_MAPS_API_KEY"/>
```

**iOS:** `ios/Runner/AppDelegate.swift`
```swift
GMSServices.provideAPIKey("YOUR_GOOGLE_MAPS_API_KEY")
```

## Debugging Tips

### Common Issues & Solutions

1. **GPS not working:**
   - Check permissions in AndroidManifest.xml and Info.plist
   - Request runtime permissions
   - Test on physical device, not emulator

2. **Database connection error:**
   - Verify PostgreSQL is running: `pg_isready`
   - Check connection string in .env
   - Ensure database exists

3. **CORS error:**
   - Add allowed origins in FastAPI CORS middleware
   - Check if backend is running

4. **Token expiration:**
   - Implement token refresh logic
   - Check token expiration time in config

## Performance Optimization

### Backend:
- Add Redis caching for leaderboards
- Use database indexes on frequently queried fields
- Implement pagination for large lists
- Use background tasks for heavy computations

### Frontend:
- Lazy load images with CachedNetworkImage
- Implement infinite scroll for lists
- Use const constructors where possible
- Optimize Google Maps rendering

## Security Checklist

- [ ] All passwords are hashed with bcrypt
- [ ] JWT tokens expire after 24 hours
- [ ] API keys are in environment variables, not code
- [ ] HTTPS only in production
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (use ORM)
- [ ] Rate limiting implemented
- [ ] Sensitive data encrypted at rest

## Deployment Checklist

### Backend:
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Gunicorn/Uvicorn workers configured
- [ ] Nginx reverse proxy setup
- [ ] SSL certificate installed
- [ ] Logging configured (Sentry)
- [ ] Health check endpoint responding

### Frontend:
- [ ] API base URL points to production
- [ ] Google Maps API key restrictions set
- [ ] App signed for release
- [ ] Privacy policy added
- [ ] Terms of service added
- [ ] App store metadata prepared

## Monitoring

### Key Metrics to Track:
- API response times
- Error rates
- GPS accuracy
- Battle completion rate
- User retention
- Crash reports

### Tools:
- Backend: Sentry, Loguru
- Frontend: Firebase Crashlytics, Firebase Analytics
- Database: pg_stat_statements
- Redis: redis-cli MONITOR

## Next Steps After MVP

Once Phase 1-6 are complete:

1. **Add Virtual Marathons**
   - User-created events
   - Entry fees and prizes

2. **Implement Premium Subscription**
   - Stripe integration
   - Feature gating

3. **Add Social Features**
   - Follow/unfollow users
   - Activity feed
   - Comments and likes

4. **Advanced Analytics**
   - Training plans
   - Progress tracking
   - Performance insights

5. **Marketing Features**
   - Referral system
   - Achievements/badges
   - Daily challenges

## Resources

- **Flutter Documentation**: https://flutter.dev/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Google Maps Flutter**: https://pub.dev/packages/google_maps_flutter
- **Geolocator Package**: https://pub.dev/packages/geolocator
- **SQLAlchemy**: https://docs.sqlalchemy.org
- **Alembic**: https://alembic.sqlalchemy.org
- **Strava API**: https://developers.strava.com

## Support

For issues during development:
1. Check error messages carefully
2. Search Stack Overflow
3. Consult official documentation
4. Review specification file

---

**Remember**: Build incrementally, test thoroughly, and don't skip steps. Each phase builds on the previous one. Good luck! 🚀
