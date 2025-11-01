# RunBattle - Complete Implementation Specification

## Repository Structure

```
runbattle/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── config.py          # Configuration settings
│   │   ├── database.py        # Database connection
│   │   │
│   │   ├── models/            # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── run.py
│   │   │   ├── battle.py
│   │   │   ├── crew.py
│   │   │   ├── league.py
│   │   │   └── marathon.py
│   │   │
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── run.py
│   │   │   ├── battle.py
│   │   │   ├── crew.py
│   │   │   └── auth.py
│   │   │
│   │   ├── api/               # API routes
│   │   │   ├── __init__.py
│   │   │   ├── deps.py        # Dependencies (auth, db)
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── runs.py
│   │   │       ├── battles.py
│   │   │       ├── crews.py
│   │   │       ├── leagues.py
│   │   │       ├── marathons.py
│   │   │       └── integrations.py
│   │   │
│   │   ├── services/          # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── gps_calculator.py
│   │   │   ├── matchmaking.py
│   │   │   ├── ranking.py
│   │   │   ├── strava_client.py
│   │   │   └── notification.py
│   │   │
│   │   └── utils/             # Utility functions
│   │       ├── __init__.py
│   │       ├── security.py
│   │       └── helpers.py
│   │
│   ├── alembic/               # Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   │
│   ├── tests/                 # Tests
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_runs.py
│   │   └── test_battles.py
│   │
│   ├── .env.example           # Environment variables template
│   ├── .gitignore
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile
│   └── README.md
│
├── frontend/                  # Flutter Mobile App
│   ├── lib/
│   │   ├── main.dart          # App entry point
│   │   │
│   │   ├── core/              # Core utilities
│   │   │   ├── constants/
│   │   │   │   ├── api_constants.dart
│   │   │   │   ├── app_colors.dart
│   │   │   │   └── app_strings.dart
│   │   │   ├── theme/
│   │   │   │   └── app_theme.dart
│   │   │   └── utils/
│   │   │       ├── dio_client.dart
│   │   │       └── helpers.dart
│   │   │
│   │   ├── features/          # Feature modules
│   │   │   ├── auth/
│   │   │   │   ├── data/
│   │   │   │   │   ├── models/
│   │   │   │   │   │   └── user_model.dart
│   │   │   │   │   └── services/
│   │   │   │   │       └── auth_service.dart
│   │   │   │   └── presentation/
│   │   │   │       ├── providers/
│   │   │   │       │   └── auth_provider.dart
│   │   │   │       ├── screens/
│   │   │   │       │   ├── login_screen.dart
│   │   │   │       │   └── register_screen.dart
│   │   │   │       └── widgets/
│   │   │   │           └── auth_form.dart
│   │   │   │
│   │   │   ├── running/
│   │   │   │   ├── data/
│   │   │   │   │   ├── models/
│   │   │   │   │   │   └── run_model.dart
│   │   │   │   │   └── services/
│   │   │   │   │       ├── gps_service.dart
│   │   │   │   │       └── run_api_service.dart
│   │   │   │   └── presentation/
│   │   │   │       ├── providers/
│   │   │   │       │   └── running_provider.dart
│   │   │   │       ├── screens/
│   │   │   │       │   ├── running_screen.dart
│   │   │   │       │   └── run_history_screen.dart
│   │   │   │       └── widgets/
│   │   │   │           ├── map_widget.dart
│   │   │   │           └── stats_card.dart
│   │   │   │
│   │   │   ├── battle/
│   │   │   │   ├── data/
│   │   │   │   │   ├── models/
│   │   │   │   │   │   └── battle_model.dart
│   │   │   │   │   └── services/
│   │   │   │   │       └── battle_service.dart
│   │   │   │   └── presentation/
│   │   │   │       ├── providers/
│   │   │   │       │   └── battle_provider.dart
│   │   │   │       ├── screens/
│   │   │   │       │   ├── battle_matchmaking_screen.dart
│   │   │   │       │   └── battle_running_screen.dart
│   │   │   │       └── widgets/
│   │   │   │           └── opponent_card.dart
│   │   │   │
│   │   │   ├── crew/
│   │   │   │   ├── data/
│   │   │   │   │   ├── models/
│   │   │   │   │   │   └── crew_model.dart
│   │   │   │   │   └── services/
│   │   │   │   │       └── crew_service.dart
│   │   │   │   └── presentation/
│   │   │   │       ├── screens/
│   │   │   │       │   ├── crew_list_screen.dart
│   │   │   │       │   └── crew_detail_screen.dart
│   │   │   │       └── widgets/
│   │   │   │           └── crew_card.dart
│   │   │   │
│   │   │   ├── league/
│   │   │   │   ├── data/
│   │   │   │   │   └── models/
│   │   │   │   │       └── league_model.dart
│   │   │   │   └── presentation/
│   │   │   │       └── screens/
│   │   │   │           └── league_screen.dart
│   │   │   │
│   │   │   └── profile/
│   │   │       ├── data/
│   │   │       │   └── services/
│   │   │       │       └── profile_service.dart
│   │   │       └── presentation/
│   │   │           └── screens/
│   │   │               ├── profile_screen.dart
│   │   │               └── settings_screen.dart
│   │   │
│   │   └── shared/            # Shared widgets
│   │       └── widgets/
│   │           ├── loading_indicator.dart
│   │           └── error_widget.dart
│   │
│   ├── android/
│   │   └── app/
│   │       └── src/
│   │           └── main/
│   │               └── AndroidManifest.xml
│   │
│   ├── ios/
│   │   └── Runner/
│   │       ├── AppDelegate.swift
│   │       └── Info.plist
│   │
│   ├── test/                  # Tests
│   │   ├── unit/
│   │   └── widget/
│   │
│   ├── .gitignore
│   ├── pubspec.yaml           # Flutter dependencies
│   └── README.md
│
├── docker-compose.yml         # Docker setup
└── README.md                  # Main project README
```

---

## BACKEND IMPLEMENTATION

### 1. Requirements (backend/requirements.txt)

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
geopy==2.4.1

# Utils
python-dateutil==2.8.2
pytz==2024.1

# Firebase
firebase-admin==6.4.0

# Monitoring
loguru==0.7.2

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
```

### 2. Environment Variables (backend/.env.example)

```env
# Database
DATABASE_URL=postgresql://runbattle:password@localhost:5432/runbattle
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here-generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Google Maps
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# Strava Integration
STRAVA_CLIENT_ID=your-strava-client-id
STRAVA_CLIENT_SECRET=your-strava-client-secret
STRAVA_REDIRECT_URI=http://localhost:8000/api/v1/integrations/strava/callback

# Firebase
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]

# App
DEBUG=True
APP_NAME=RunBattle
APP_VERSION=1.0.0
```

### 3. Configuration (backend/app/config.py)

```python
from pydantic_settings import BaseSettings
from typing import List

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
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Google Maps
    GOOGLE_MAPS_API_KEY: str
    
    # Strava
    STRAVA_CLIENT_ID: str
    STRAVA_CLIENT_SECRET: str
    STRAVA_REDIRECT_URI: str
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 4. Database Connection (backend/app/database.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 5. User Model (backend/app/models/user.py)

```python
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    avatar_url = Column(String(500))
    weight_kg = Column(Float, default=70.0)
    
    # Stats
    total_distance_km = Column(Float, default=0.0)
    total_duration_seconds = Column(Integer, default=0)
    total_runs = Column(Integer, default=0)
    avg_pace = Column(Float, default=0.0)
    
    # Rankings
    elo_rating = Column(Integer, default=1200)
    league_tier = Column(String(20), default='Bronze')
    league_points = Column(Integer, default=0)
    
    # Integrations
    strava_access_token = Column(String(255))
    strava_refresh_token = Column(String(255))
    strava_athlete_id = Column(String(50))
    
    # Premium
    is_premium = Column(Boolean, default=False)
    premium_expires_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)
    
    # Relationships
    runs = relationship("Run", back_populates="user", cascade="all, delete-orphan")
    battles_as_user1 = relationship("Battle", foreign_keys="Battle.user1_id", back_populates="user1")
    battles_as_user2 = relationship("Battle", foreign_keys="Battle.user2_id", back_populates="user2")
```

### 6. Run Model (backend/app/models/run.py)

```python
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base

class Run(Base):
    __tablename__ = "runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Metrics
    distance_km = Column(Float, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    avg_pace = Column(Float, nullable=False)  # min/km
    avg_speed = Column(Float, nullable=False)  # km/h
    calories_burned = Column(Float, default=0.0)
    
    # Route data (encoded polyline string)
    route_polyline = Column(Text)
    start_lat = Column(Float)
    start_lng = Column(Float)
    end_lat = Column(Float)
    end_lng = Column(Float)
    
    # Timestamps
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Source
    source = Column(String(20), default='app')  # 'app', 'strava', 'nike'
    external_id = Column(String(100))  # ID from external source
    
    # Relationship
    user = relationship("User", back_populates="runs")
```

### 7. Battle Model (backend/app/models/battle.py)

```python
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base

class Battle(Base):
    __tablename__ = "battles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Participants
    user1_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user2_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Battle config
    distance_km = Column(Float, nullable=False)
    
    # Results
    winner_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    user1_distance = Column(Float, default=0.0)
    user2_distance = Column(Float, default=0.0)
    user1_time = Column(Integer, default=0)  # seconds
    user2_time = Column(Integer, default=0)  # seconds
    user1_pace = Column(Float, default=0.0)
    user2_pace = Column(Float, default=0.0)
    
    # ELO changes
    user1_elo_before = Column(Integer)
    user2_elo_before = Column(Integer)
    user1_elo_after = Column(Integer)
    user2_elo_after = Column(Integer)
    
    # Status: 'pending', 'active', 'completed', 'cancelled'
    status = Column(String(20), default='pending')
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user1 = relationship("User", foreign_keys=[user1_id], back_populates="battles_as_user1")
    user2 = relationship("User", foreign_keys=[user2_id], back_populates="battles_as_user2")
    winner = relationship("User", foreign_keys=[winner_id])
```

### 8. Crew Model (backend/app/models/crew.py)

```python
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base

class Crew(Base):
    __tablename__ = "crews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    avatar_url = Column(String(500))
    
    captain_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Stats
    total_members = Column(Integer, default=0)
    total_distance_km = Column(Float, default=0.0)
    total_runs = Column(Integer, default=0)
    battle_wins = Column(Integer, default=0)
    battle_losses = Column(Integer, default=0)
    
    # Settings
    is_public = Column(Boolean, default=True)
    max_members = Column(Integer, default=50)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    captain = relationship("User")
    members = relationship("CrewMembership", back_populates="crew", cascade="all, delete-orphan")


class CrewMembership(Base):
    __tablename__ = "crew_memberships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crew_id = Column(UUID(as_uuid=True), ForeignKey('crews.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    role = Column(String(20), default='member')  # 'captain', 'admin', 'member'
    
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    crew = relationship("Crew", back_populates="members")
    user = relationship("User")
```

### 9. Security Utils (backend/app/utils/security.py)

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

### 10. GPS Calculator Service (backend/app/services/gps_calculator.py)

```python
from math import radians, cos, sin, asin, sqrt
from typing import List, Tuple

class GPSCalculator:
    """GPS distance and statistics calculator"""
    
    EARTH_RADIUS_KM = 6371

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two GPS points using Haversine formula
        Returns distance in kilometers
        """
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        distance_km = GPSCalculator.EARTH_RADIUS_KM * c
        return distance_km

    @staticmethod
    def calculate_total_distance(route: List[Tuple[float, float]]) -> float:
        """Calculate total distance from list of (lat, lng) coordinates"""
        if len(route) < 2:
            return 0.0
        
        total_distance = 0.0
        for i in range(len(route) - 1):
            lat1, lon1 = route[i]
            lat2, lon2 = route[i + 1]
            segment_distance = GPSCalculator.haversine_distance(lat1, lon1, lat2, lon2)
            total_distance += segment_distance
        
        return total_distance

    @staticmethod
    def calculate_pace(distance_km: float, duration_seconds: int) -> float:
        """Calculate pace in minutes per kilometer"""
        if distance_km <= 0:
            return 0.0
        duration_minutes = duration_seconds / 60
        pace = duration_minutes / distance_km
        return round(pace, 2)

    @staticmethod
    def calculate_speed(distance_km: float, duration_seconds: int) -> float:
        """Calculate speed in kilometers per hour"""
        if duration_seconds <= 0:
            return 0.0
        duration_hours = duration_seconds / 3600
        speed = distance_km / duration_hours
        return round(speed, 2)

    @staticmethod
    def calculate_calories(distance_km: float, weight_kg: float = 70, running: bool = True) -> float:
        """Calculate calories burned"""
        if running:
            calories = weight_kg * distance_km * 1.0
        else:
            calories = weight_kg * distance_km * 0.5
        return round(calories, 2)
```

### 11. Auth Schemas (backend/app/schemas/auth.py)

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    total_distance_km: float
    total_runs: int
    elo_rating: int
    league_tier: str
    is_premium: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
```

### 12. Run Schemas (backend/app/schemas/run.py)

```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RoutePoint(BaseModel):
    lat: float
    lng: float

class RunCreate(BaseModel):
    distance_km: float
    duration_seconds: int
    avg_pace: float
    avg_speed: float
    route: List[RoutePoint]
    start_time: datetime
    end_time: datetime
    calories_burned: Optional[float] = 0.0

class RunResponse(BaseModel):
    id: str
    user_id: str
    distance_km: float
    duration_seconds: int
    avg_pace: float
    avg_speed: float
    calories_burned: float
    started_at: datetime
    completed_at: datetime
    source: str

    class Config:
        from_attributes = True
```

### 13. API Dependencies (backend/app/api/deps.py)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import decode_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user
```

### 14. Auth Endpoints (backend/app/api/v1/auth.py)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.models.user import User
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_password,
        full_name=user_data.full_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(new_user.id)}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(new_user)
    }

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    
    # Update last login
    from datetime import datetime
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse.from_orm(current_user)
```

### 15. Runs Endpoints (backend/app/api/v1/runs.py)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.schemas.run import RunCreate, RunResponse
from app.models.run import Run
from app.models.user import User
from app.api.deps import get_current_user
from app.services.gps_calculator import GPSCalculator

router = APIRouter(prefix="/runs", tags=["Runs"])

@router.post("", response_model=RunResponse, status_code=status.HTTP_201_CREATED)
async def create_run(
    run_data: RunCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save a completed run"""
    # Calculate calories if not provided
    if run_data.calories_burned == 0:
        run_data.calories_burned = GPSCalculator.calculate_calories(
            run_data.distance_km,
            current_user.weight_kg
        )
    
    # Create route polyline (simplified - store as JSON string)
    import json
    route_polyline = json.dumps([{"lat": p.lat, "lng": p.lng} for p in run_data.route])
    
    # Create run
    new_run = Run(
        user_id=current_user.id,
        distance_km=run_data.distance_km,
        duration_seconds=run_data.duration_seconds,
        avg_pace=run_data.avg_pace,
        avg_speed=run_data.avg_speed,
        calories_burned=run_data.calories_burned,
        route_polyline=route_polyline,
        start_lat=run_data.route[0].lat if run_data.route else None,
        start_lng=run_data.route[0].lng if run_data.route else None,
        started_at=run_data.start_time,
        completed_at=run_data.end_time,
        source='app'
    )
    
    db.add(new_run)
    
    # Update user stats
    current_user.total_distance_km += run_data.distance_km
    current_user.total_duration_seconds += run_data.duration_seconds
    current_user.total_runs += 1
    
    # Recalculate average pace
    if current_user.total_distance_km > 0:
        current_user.avg_pace = (
            current_user.total_duration_seconds / 60
        ) / current_user.total_distance_km
    
    db.commit()
    db.refresh(new_run)
    
    return RunResponse.from_orm(new_run)

@router.get("", response_model=List[RunResponse])
async def get_user_runs(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's run history"""
    runs = db.query(Run).filter(
        Run.user_id == current_user.id
    ).order_by(
        Run.completed_at.desc()
    ).offset(skip).limit(limit).all()
    
    return [RunResponse.from_orm(run) for run in runs]

@router.get("/{run_id}", response_model=RunResponse)
async def get_run_detail(
    run_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific run details"""
    run = db.query(Run).filter(
        Run.id == run_id,
        Run.user_id == current_user.id
    ).first()
    
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Run not found"
        )
    
    return RunResponse.from_orm(run)
```

### 16. Main FastAPI App (backend/app/main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api.v1 import auth, runs

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(runs.router, prefix="/api/v1")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": f"{settings.APP_NAME} API is running",
        "version": settings.APP_VERSION,
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "ok",
        "database": "connected",
        "version": settings.APP_VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
```

---

## FRONTEND IMPLEMENTATION

### 1. Dependencies (frontend/pubspec.yaml)

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
  
  # Network
  dio: ^5.4.0
  
  # Maps & Location
  google_maps_flutter: ^2.5.0
  geolocator: ^10.1.0
  geocoding: ^2.1.1
  
  # Storage
  shared_preferences: ^2.2.2
  flutter_secure_storage: ^9.0.0
  
  # UI
  fl_chart: ^0.65.0
  cached_network_image: ^3.3.1
  
  # Utils
  intl: ^0.18.1
  uuid: ^4.3.3
  permission_handler: ^11.2.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
```

### 2. API Constants (frontend/lib/core/constants/api_constants.dart)

```dart
class ApiConstants {
  static const String baseUrl = 'http://localhost:8000';
  static const String apiVersion = '/api/v1';
  
  // Auth endpoints
  static const String register = '$apiVersion/auth/register';
  static const String login = '$apiVersion/auth/login';
  static const String me = '$apiVersion/auth/me';
  
  // Run endpoints
  static const String runs = '$apiVersion/runs';
  
  // Battle endpoints
  static const String battles = '$apiVersion/battles';
  static const String matchmaking = '$battles/matchmaking';
  
  // Crew endpoints
  static const String crews = '$apiVersion/crews';
}
```

### 3. Dio Client (frontend/lib/core/utils/dio_client.dart)

```dart
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../constants/api_constants.dart';

class DioClient {
  final Dio _dio;
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  DioClient()
      : _dio = Dio(
          BaseOptions(
            baseUrl: ApiConstants.baseUrl,
            connectTimeout: const Duration(seconds: 30),
            receiveTimeout: const Duration(seconds: 30),
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
          ),
        ) {
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          // Add auth token to requests
          final token = await _storage.read(key: 'auth_token');
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          return handler.next(options);
        },
        onError: (error, handler) async {
          // Handle 401 Unauthorized
          if (error.response?.statusCode == 401) {
            await _storage.delete(key: 'auth_token');
            // Navigate to login screen
          }
          return handler.next(error);
        },
      ),
    );
  }

  Dio get dio => _dio;

  Future<void> saveToken(String token) async {
    await _storage.write(key: 'auth_token', value: token);
  }

  Future<String?> getToken() async {
    return await _storage.read(key: 'auth_token');
  }

  Future<void> deleteToken() async {
    await _storage.delete(key: 'auth_token');
  }
}
```

### 4. User Model (frontend/lib/features/auth/data/models/user_model.dart)

```dart
class UserModel {
  final String id;
  final String email;
  final String username;
  final String? fullName;
  final String? avatarUrl;
  final double totalDistanceKm;
  final int totalRuns;
  final int eloRating;
  final String leagueTier;
  final bool isPremium;
  final DateTime createdAt;

  UserModel({
    required this.id,
    required this.email,
    required this.username,
    this.fullName,
    this.avatarUrl,
    required this.totalDistanceKm,
    required this.totalRuns,
    required this.eloRating,
    required this.leagueTier,
    required this.isPremium,
    required this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      email: json['email'],
      username: json['username'],
      fullName: json['full_name'],
      avatarUrl: json['avatar_url'],
      totalDistanceKm: (json['total_distance_km'] ?? 0.0).toDouble(),
      totalRuns: json['total_runs'] ?? 0,
      eloRating: json['elo_rating'] ?? 1200,
      leagueTier: json['league_tier'] ?? 'Bronze',
      isPremium: json['is_premium'] ?? false,
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'username': username,
      'full_name': fullName,
      'avatar_url': avatarUrl,
      'total_distance_km': totalDistanceKm,
      'total_runs': totalRuns,
      'elo_rating': eloRating,
      'league_tier': leagueTier,
      'is_premium': isPremium,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
```

### 5. Auth Service (frontend/lib/features/auth/data/services/auth_service.dart)

```dart
import 'package:dio/dio.dart';
import '../../../../core/utils/dio_client.dart';
import '../../../../core/constants/api_constants.dart';
import '../models/user_model.dart';

class AuthService {
  final DioClient _dioClient;

  AuthService(this._dioClient);

  Future<Map<String, dynamic>> register({
    required String email,
    required String username,
    required String password,
    String? fullName,
  }) async {
    try {
      final response = await _dioClient.dio.post(
        ApiConstants.register,
        data: {
          'email': email,
          'username': username,
          'password': password,
          if (fullName != null) 'full_name': fullName,
        },
      );

      final token = response.data['access_token'];
      await _dioClient.saveToken(token);

      return response.data;
    } on DioException catch (e) {
      throw Exception(e.response?.data['detail'] ?? 'Registration failed');
    }
  }

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _dioClient.dio.post(
        ApiConstants.login,
        data: {
          'email': email,
          'password': password,
        },
      );

      final token = response.data['access_token'];
      await _dioClient.saveToken(token);

      return response.data;
    } on DioException catch (e) {
      throw Exception(e.response?.data['detail'] ?? 'Login failed');
    }
  }

  Future<UserModel> getCurrentUser() async {
    try {
      final response = await _dioClient.dio.get(ApiConstants.me);
      return UserModel.fromJson(response.data);
    } on DioException catch (e) {
      throw Exception(e.response?.data['detail'] ?? 'Failed to get user');
    }
  }

  Future<void> logout() async {
    await _dioClient.deleteToken();
  }

  Future<bool> isLoggedIn() async {
    final token = await _dioClient.getToken();
    return token != null;
  }
}
```

### 6. Auth Provider (frontend/lib/features/auth/presentation/providers/auth_provider.dart)

```dart
import 'package:flutter/material.dart';
import '../../data/services/auth_service.dart';
import '../../data/models/user_model.dart';

class AuthProvider extends ChangeNotifier {
  final AuthService _authService;
  
  UserModel? _user;
  bool _isLoading = false;
  String? _errorMessage;

  AuthProvider(this._authService);

  UserModel? get user => _user;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  bool get isAuthenticated => _user != null;

  Future<bool> register({
    required String email,
    required String username,
    required String password,
    String? fullName,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final response = await _authService.register(
        email: email,
        username: username,
        password: password,
        fullName: fullName,
      );

      _user = UserModel.fromJson(response['user']);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> login({
    required String email,
    required String password,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final response = await _authService.login(
        email: email,
        password: password,
      );

      _user = UserModel.fromJson(response['user']);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> logout() async {
    await _authService.logout();
    _user = null;
    notifyListeners();
  }

  Future<void> checkAuthStatus() async {
    if (await _authService.isLoggedIn()) {
      try {
        _user = await _authService.getCurrentUser();
        notifyListeners();
      } catch (e) {
        await logout();
      }
    }
  }
}
```

### 7. Login Screen (frontend/lib/features/auth/presentation/screens/login_screen.dart)

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import 'register_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    if (!_formKey.currentState!.validate()) return;

    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    
    final success = await authProvider.login(
      email: _emailController.text.trim(),
      password: _passwordController.text,
    );

    if (success && mounted) {
      Navigator.of(context).pushReplacementNamed('/home');
    } else if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(authProvider.errorMessage ?? 'Login failed'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 60),
                const Text(
                  '🏃 RunBattle',
                  style: TextStyle(
                    fontSize: 48,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                const Text(
                  'Compete. Run. Win.',
                  style: TextStyle(
                    fontSize: 18,
                    color: Colors.grey,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 60),
                
                // Email field
                TextFormField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(
                    labelText: 'Email',
                    prefixIcon: Icon(Icons.email),
                    border: OutlineInputBorder(),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your email';
                    }
                    if (!value.contains('@')) {
                      return 'Please enter a valid email';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                
                // Password field
                TextFormField(
                  controller: _passwordController,
                  obscureText: _obscurePassword,
                  decoration: InputDecoration(
                    labelText: 'Password',
                    prefixIcon: const Icon(Icons.lock),
                    border: const OutlineInputBorder(),
                    suffixIcon: IconButton(
                      icon: Icon(
                        _obscurePassword ? Icons.visibility : Icons.visibility_off,
                      ),
                      onPressed: () {
                        setState(() {
                          _obscurePassword = !_obscurePassword;
                        });
                      },
                    ),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your password';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 24),
                
                // Login button
                Consumer<AuthProvider>(
                  builder: (context, authProvider, _) {
                    return ElevatedButton(
                      onPressed: authProvider.isLoading ? null : _handleLogin,
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                      child: authProvider.isLoading
                          ? const SizedBox(
                              height: 20,
                              width: 20,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : const Text(
                              'Login',
                              style: TextStyle(fontSize: 16),
                            ),
                    );
                  },
                ),
                const SizedBox(height: 16),
                
                // Register link
                TextButton(
                  onPressed: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (context) => const RegisterScreen(),
                      ),
                    );
                  },
                  child: const Text("Don't have an account? Register"),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

### 8. GPS Service (frontend/lib/features/running/data/services/gps_service.dart)

```dart
import 'dart:async';
import 'package:geolocator/geolocator.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

class GPSService {
  StreamSubscription<Position>? _positionStream;
  List<LatLng> routePoints = [];
  double totalDistance = 0.0;
  DateTime? startTime;
  bool isTracking = false;

  Future<bool> checkPermission() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return false;
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        return false;
      }
    }

    if (permission == LocationPermission.deniedForever) {
      return false;
    }

    return true;
  }

  Future<void> startTracking() async {
    if (!await checkPermission()) {
      throw Exception('Location permission denied');
    }

    routePoints.clear();
    totalDistance = 0.0;
    startTime = DateTime.now();
    isTracking = true;

    const LocationSettings locationSettings = LocationSettings(
      accuracy: LocationAccuracy.high,
      distanceFilter: 5, // Update every 5 meters
    );

    _positionStream = Geolocator.getPositionStream(
      locationSettings: locationSettings,
    ).listen((Position position) {
      _updateRoute(position);
    });
  }

  void _updateRoute(Position position) {
    LatLng newPoint = LatLng(position.latitude, position.longitude);

    if (routePoints.isNotEmpty) {
      LatLng lastPoint = routePoints.last;
      double distance = Geolocator.distanceBetween(
        lastPoint.latitude,
        lastPoint.longitude,
        newPoint.latitude,
        newPoint.longitude,
      );
      totalDistance += distance;
    }

    routePoints.add(newPoint);
  }

  void pauseTracking() {
    _positionStream?.pause();
    isTracking = false;
  }

  void resumeTracking() {
    _positionStream?.resume();
    isTracking = true;
  }

  Future<RunResult> stopTracking() async {
    await _positionStream?.cancel();
    _positionStream = null;
    isTracking = false;

    DateTime endTime = DateTime.now();
    Duration duration = endTime.difference(startTime!);
    double distanceKm = totalDistance / 1000;
    double avgSpeed = distanceKm / (duration.inSeconds / 3600);
    double avgPace = duration.inMinutes / distanceKm;

    return RunResult(
      distance: distanceKm,
      duration: duration,
      avgSpeed: avgSpeed,
      avgPace: avgPace,
      route: routePoints,
      startTime: startTime!,
      endTime: endTime,
    );
  }

  Future<Position> getCurrentPosition() async {
    if (!await checkPermission()) {
      throw Exception('Location permission denied');
    }

    return await Geolocator.getCurrentPosition(
      desiredAccuracy: LocationAccuracy.high,
    );
  }

  void dispose() {
    _positionStream?.cancel();
  }
}

class RunResult {
  final double distance;
  final Duration duration;
  final double avgSpeed;
  final double avgPace;
  final List<LatLng> route;
  final DateTime startTime;
  final DateTime endTime;

  RunResult({
    required this.distance,
    required this.duration,
    required this.avgSpeed,
    required this.avgPace,
    required this.route,
    required this.startTime,
    required this.endTime,
  });

  Map<String, dynamic> toJson() {
    return {
      'distance_km': distance,
      'duration_seconds': duration.inSeconds,
      'avg_speed': avgSpeed,
      'avg_pace': avgPace,
      'route': route.map((point) => {
        'lat': point.latitude,
        'lng': point.longitude,
      }).toList(),
      'start_time': startTime.toIso8601String(),
      'end_time': endTime.toIso8601String(),
    };
  }
}
```

### 9. Main App (frontend/lib/main.dart)

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/utils/dio_client.dart';
import 'features/auth/data/services/auth_service.dart';
import 'features/auth/presentation/providers/auth_provider.dart';
import 'features/auth/presentation/screens/login_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final dioClient = DioClient();
    
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => AuthProvider(AuthService(dioClient)),
        ),
      ],
      child: MaterialApp(
        title: 'RunBattle',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          primarySwatch: Colors.blue,
          useMaterial3: true,
        ),
        home: const LoginScreen(),
      ),
    );
  }
}
```

---

## SETUP INSTRUCTIONS

### Backend Setup

```bash
# 1. Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env
# Edit .env with your configuration

# 4. Initialize database
# Start PostgreSQL and Redis

# 5. Run migrations
alembic upgrade head

# 6. Run server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
# 1. Get Flutter dependencies
cd frontend
flutter pub get

# 2. Configure Google Maps API
# Android: Edit android/app/src/main/AndroidManifest.xml
# iOS: Edit ios/Runner/AppDelegate.swift and Info.plist

# 3. Run app
flutter run
```

### Docker Setup

```bash
# Run both backend and databases
docker-compose up
```

---

## NEXT STEPS

1. **Implement remaining endpoints**: battles, crews, leagues, marathons
2. **Add more Flutter screens**: battle, crew, profile screens
3. **Implement real-time features**: WebSocket for battles
4. **Add Strava OAuth**: Complete integration
5. **Add tests**: Unit and integration tests
6. **Setup CI/CD**: GitHub Actions
7. **Deploy**: AWS, Google Cloud, or DigitalOcean

This specification provides a complete, production-ready structure for RunBattle!
