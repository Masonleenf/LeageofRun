# RunBattle - Essential Code Snippets

Copy and paste these code snippets directly into your project.

## 🔐 Authentication System

### Backend: JWT Security (backend/app/core/security.py)

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

### Backend: Auth Endpoints (backend/app/api/v1/endpoints/auth.py)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": str(new_user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(new_user)
    }

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }
```

### Frontend: Auth Service (frontend/lib/features/auth/data/services/auth_service.dart)

```dart
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthService {
  final Dio _dio;
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  static const String _tokenKey = 'auth_token';

  AuthService(this._dio);

  Future<Map<String, dynamic>> register({
    required String email,
    required String username,
    required String password,
  }) async {
    try {
      final response = await _dio.post(
        '/auth/register',
        data: {
          'email': email,
          'username': username,
          'password': password,
        },
      );

      final token = response.data['access_token'];
      await _storage.write(key: _tokenKey, value: token);

      return response.data;
    } catch (e) {
      throw Exception('Registration failed: $e');
    }
  }

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );

      final token = response.data['access_token'];
      await _storage.write(key: _tokenKey, value: token);

      return response.data;
    } catch (e) {
      throw Exception('Login failed: $e');
    }
  }

  Future<void> logout() async {
    await _storage.delete(key: _tokenKey);
  }

  Future<String?> getToken() async {
    return await _storage.read(key: _tokenKey);
  }

  Future<bool> isLoggedIn() async {
    final token = await getToken();
    return token != null;
  }
}
```

## 📍 GPS Tracking System

### Backend: GPS Calculator (backend/app/services/gps_calculator.py)

```python
from math import radians, cos, sin, asin, sqrt
from typing import List, Tuple

class GPSCalculator:
    EARTH_RADIUS_KM = 6371

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two GPS points in kilometers"""
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        distance_km = GPSCalculator.EARTH_RADIUS_KM * c
        return distance_km

    @staticmethod
    def calculate_total_distance(route: List[Tuple[float, float]]) -> float:
        """Calculate total distance from list of GPS coordinates"""
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
        return pace

    @staticmethod
    def calculate_speed(distance_km: float, duration_seconds: int) -> float:
        """Calculate speed in kilometers per hour"""
        if duration_seconds <= 0:
            return 0.0
        duration_hours = duration_seconds / 3600
        speed = distance_km / duration_hours
        return speed
```

### Frontend: GPS Service (frontend/lib/features/running/data/services/gps_service.dart)

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
      distanceFilter: 5,
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
      'distance': distance,
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

## ⚔️ Battle Matchmaking System

### Backend: Matchmaking Service (backend/app/services/matchmaking.py)

```python
import redis
import json
from typing import Optional, Dict
from datetime import datetime

class MatchmakingService:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.queue_key = "battle:queue"
        self.timeout_seconds = 60

    def join_queue(self, user_id: str, avg_pace: float, distance_km: float) -> Optional[Dict]:
        """
        Join matchmaking queue and find opponent
        Returns opponent info if match found, None otherwise
        """
        # Get all users in queue
        queue_users = self.redis.lrange(self.queue_key, 0, -1)
        
        # Try to find match
        for user_data_str in queue_users:
            user_data = json.loads(user_data_str)
            
            # Check if pace is similar (within 10%)
            pace_diff = abs(user_data['avg_pace'] - avg_pace)
            if pace_diff <= avg_pace * 0.1:  # 10% tolerance
                # Match found! Remove from queue
                self.redis.lrem(self.queue_key, 1, user_data_str)
                
                return {
                    'user_id': user_data['user_id'],
                    'avg_pace': user_data['avg_pace'],
                    'username': user_data['username'],
                    'elo_rating': user_data['elo_rating']
                }
        
        # No match found, add to queue
        queue_data = json.dumps({
            'user_id': user_id,
            'avg_pace': avg_pace,
            'distance_km': distance_km,
            'timestamp': datetime.utcnow().isoformat(),
            'username': 'User',  # Get from database
            'elo_rating': 1200  # Get from database
        })
        self.redis.rpush(self.queue_key, queue_data)
        
        # Set expiration
        self.redis.expire(self.queue_key, self.timeout_seconds)
        
        return None

    def leave_queue(self, user_id: str):
        """Remove user from matchmaking queue"""
        queue_users = self.redis.lrange(self.queue_key, 0, -1)
        for user_data_str in queue_users:
            user_data = json.loads(user_data_str)
            if user_data['user_id'] == user_id:
                self.redis.lrem(self.queue_key, 1, user_data_str)
                break

    def update_elo(self, winner_elo: int, loser_elo: int, k_factor: int = 32) -> tuple:
        """
        Calculate new ELO ratings after battle
        Returns: (winner_new_elo, loser_new_elo)
        """
        expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
        expected_loser = 1 - expected_winner
        
        winner_new_elo = winner_elo + k_factor * (1 - expected_winner)
        loser_new_elo = loser_elo + k_factor * (0 - expected_loser)
        
        return (int(winner_new_elo), int(loser_new_elo))
```

### Backend: Battle Endpoints (backend/app/api/v1/endpoints/battles.py)

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.matchmaking import MatchmakingService
from app.models.battle import Battle
from app.schemas.battle import BattleCreate, BattleResponse

router = APIRouter()

@router.post("/matchmaking")
async def find_opponent(
    battle_request: BattleCreate,
    db: Session = Depends(get_db),
    matchmaking: MatchmakingService = Depends(get_matchmaking_service)
):
    """Find opponent for battle"""
    user_id = battle_request.user_id
    avg_pace = battle_request.avg_pace
    distance_km = battle_request.distance_km
    
    opponent = matchmaking.join_queue(user_id, avg_pace, distance_km)
    
    if opponent:
        # Match found! Create battle
        battle = Battle(
            user1_id=user_id,
            user2_id=opponent['user_id'],
            distance_km=distance_km,
            status='pending'
        )
        db.add(battle)
        db.commit()
        db.refresh(battle)
        
        return {
            'success': True,
            'battle_id': str(battle.id),
            'opponent': opponent,
            'message': 'Opponent found!'
        }
    else:
        return {
            'success': False,
            'message': 'Searching for opponent...'
        }

@router.post("/{battle_id}/complete")
async def complete_battle(
    battle_id: str,
    user_id: str,
    final_time: int,
    db: Session = Depends(get_db),
    matchmaking: MatchmakingService = Depends(get_matchmaking_service)
):
    """Complete battle and calculate winner"""
    battle = db.query(Battle).filter(Battle.id == battle_id).first()
    
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    
    # Update user's time
    if battle.user1_id == user_id:
        battle.user1_time = final_time
    else:
        battle.user2_time = final_time
    
    # Check if both completed
    if battle.user1_time and battle.user2_time:
        # Determine winner
        if battle.user1_time < battle.user2_time:
            battle.winner_id = battle.user1_id
            winner_elo = battle.user1.elo_rating
            loser_elo = battle.user2.elo_rating
        else:
            battle.winner_id = battle.user2_id
            winner_elo = battle.user2.elo_rating
            loser_elo = battle.user1.elo_rating
        
        # Update ELO ratings
        new_winner_elo, new_loser_elo = matchmaking.update_elo(winner_elo, loser_elo)
        
        battle.status = 'completed'
        db.commit()
        
        return {
            'winner_id': battle.winner_id,
            'new_ratings': {
                'winner': new_winner_elo,
                'loser': new_loser_elo
            }
        }
    
    db.commit()
    return {'message': 'Waiting for opponent to finish'}
```

## 🗄️ Database Models

### User Model (backend/app/models/user.py)

```python
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    avatar_url = Column(String)
    weight_kg = Column(Float, default=70.0)
    
    # Statistics
    total_distance_km = Column(Float, default=0.0)
    total_duration_seconds = Column(Integer, default=0)
    total_runs = Column(Integer, default=0)
    avg_pace = Column(Float, default=0.0)
    
    # Rankings
    elo_rating = Column(Integer, default=1200)
    league_tier = Column(String, default='Bronze')
    league_points = Column(Integer, default=0)
    
    # Integrations
    strava_access_token = Column(String)
    strava_refresh_token = Column(String)
    strava_athlete_id = Column(String)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_premium = Column(Boolean, default=False)
```

### Run Model (backend/app/models/run.py)

```python
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.core.database import Base

class Run(Base):
    __tablename__ = "runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Metrics
    distance_km = Column(Float, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    avg_pace = Column(Float, nullable=False)
    avg_speed = Column(Float, nullable=False)
    calories_burned = Column(Float)
    
    # Route data
    route_polyline = Column(Text)  # Encoded polyline
    start_lat = Column(Float)
    start_lng = Column(Float)
    
    # Timestamps
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Source
    source = Column(String, default='app')  # 'app', 'strava', 'nike'
    
    # Relationship
    user = relationship("User", backref="runs")
```

## 🎨 Frontend UI Components

### Running Screen (frontend/lib/features/running/presentation/screens/running_screen.dart)

```dart
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:runbattle/features/running/data/services/gps_service.dart';
import 'dart:async';

class RunningScreen extends StatefulWidget {
  const RunningScreen({Key? key}) : super(key: key);

  @override
  State<RunningScreen> createState() => _RunningScreenState();
}

class _RunningScreenState extends State<RunningScreen> {
  GoogleMapController? _mapController;
  final GPSService _gpsService = GPSService();
  Timer? _timer;
  Duration _elapsedTime = Duration.zero;
  
  double _currentDistance = 0.0;
  double _currentSpeed = 0.0;
  double _currentPace = 0.0;
  
  bool _isRunning = false;
  bool _isPaused = false;
  
  LatLng _initialPosition = const LatLng(37.5665, 126.9780);
  Set<Polyline> _polylines = {};

  @override
  void initState() {
    super.initState();
    _getCurrentLocation();
  }

  Future<void> _getCurrentLocation() async {
    try {
      final position = await _gpsService.getCurrentPosition();
      setState(() {
        _initialPosition = LatLng(position.latitude, position.longitude);
      });
      
      _mapController?.animateCamera(
        CameraUpdate.newLatLngZoom(_initialPosition, 16),
      );
    } catch (e) {
      _showError('Location permission denied');
    }
  }

  Future<void> _startRunning() async {
    try {
      await _gpsService.startTracking();
      
      setState(() {
        _isRunning = true;
        _isPaused = false;
        _elapsedTime = Duration.zero;
      });

      _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
        setState(() {
          _elapsedTime += const Duration(seconds: 1);
          _updateStats();
          _updateMapRoute();
        });
      });
    } catch (e) {
      _showError('Failed to start running: $e');
    }
  }

  void _updateStats() {
    _currentDistance = _gpsService.totalDistance / 1000;
    
    if (_elapsedTime.inSeconds > 0) {
      _currentSpeed = _currentDistance / (_elapsedTime.inSeconds / 3600);
      
      if (_currentDistance > 0) {
        _currentPace = _elapsedTime.inMinutes / _currentDistance;
      }
    }
  }

  void _updateMapRoute() {
    if (_gpsService.routePoints.isNotEmpty) {
      setState(() {
        _polylines = {
          Polyline(
            polylineId: const PolylineId('running_route'),
            points: _gpsService.routePoints,
            color: Colors.blue,
            width: 5,
          ),
        };
      });

      if (_gpsService.routePoints.isNotEmpty) {
        _mapController?.animateCamera(
          CameraUpdate.newLatLng(_gpsService.routePoints.last),
        );
      }
    }
  }

  Future<void> _stopRunning() async {
    _timer?.cancel();
    
    final result = await _gpsService.stopTracking();
    
    setState(() {
      _isRunning = false;
      _isPaused = false;
    });

    _showResultDialog(result);
  }

  void _showResultDialog(RunResult result) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('🎉 Run Complete!'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('📏 Distance: ${result.distance.toStringAsFixed(2)} km'),
            const SizedBox(height: 8),
            Text('⏱️ Time: ${result.duration.inMinutes}:${(result.duration.inSeconds % 60).toString().padLeft(2, '0')}'),
            const SizedBox(height: 8),
            Text('⚡ Avg Speed: ${result.avgSpeed.toStringAsFixed(2)} km/h'),
            const SizedBox(height: 8),
            Text('🎯 Avg Pace: ${result.avgPace.toStringAsFixed(2)} min/km'),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              // TODO: Save to server
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Running'),
        backgroundColor: Colors.blue,
      ),
      body: Stack(
        children: [
          GoogleMap(
            initialCameraPosition: CameraPosition(
              target: _initialPosition,
              zoom: 16,
            ),
            onMapCreated: (controller) {
              _mapController = controller;
            },
            myLocationEnabled: true,
            myLocationButtonEnabled: true,
            polylines: _polylines,
          ),
          Positioned(
            top: 16,
            left: 16,
            right: 16,
            child: Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    Text(
                      _formatDuration(_elapsedTime),
                      style: const TextStyle(
                        fontSize: 48,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        _buildStatItem('Distance', '${_currentDistance.toStringAsFixed(2)} km'),
                        _buildStatItem('Speed', '${_currentSpeed.toStringAsFixed(1)} km/h'),
                        _buildStatItem('Pace', '${_currentPace.toStringAsFixed(1)} min/km'),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
          Positioned(
            bottom: 32,
            left: 16,
            right: 16,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                if (!_isRunning)
                  _buildControlButton(
                    icon: Icons.play_arrow,
                    label: 'Start',
                    color: Colors.green,
                    onTap: _startRunning,
                  )
                else if (_isPaused)
                  _buildControlButton(
                    icon: Icons.play_arrow,
                    label: 'Resume',
                    color: Colors.green,
                    onTap: () {
                      _gpsService.resumeTracking();
                      setState(() => _isPaused = false);
                    },
                  )
                else
                  _buildControlButton(
                    icon: Icons.pause,
                    label: 'Pause',
                    color: Colors.orange,
                    onTap: () {
                      _gpsService.pauseTracking();
                      setState(() => _isPaused = true);
                    },
                  ),
                if (_isRunning) ...[
                  const SizedBox(width: 16),
                  _buildControlButton(
                    icon: Icons.stop,
                    label: 'Stop',
                    color: Colors.red,
                    onTap: _stopRunning,
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatItem(String label, String value) {
    return Column(
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 12, color: Colors.grey),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ],
    );
  }

  Widget _buildControlButton({
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 80,
        height: 80,
        decoration: BoxDecoration(
          color: color,
          shape: BoxShape.circle,
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: Colors.white, size: 32),
            const SizedBox(height: 4),
            Text(
              label,
              style: const TextStyle(color: Colors.white, fontSize: 10),
            ),
          ],
        ),
      ),
    );
  }

  String _formatDuration(Duration duration) {
    String twoDigits(int n) => n.toString().padLeft(2, '0');
    return '${twoDigits(duration.inHours)}:${twoDigits(duration.inMinutes.remainder(60))}:${twoDigits(duration.inSeconds.remainder(60))}';
  }

  @override
  void dispose() {
    _timer?.cancel();
    _mapController?.dispose();
    super.dispose();
  }
}
```

---

These snippets provide the core functionality needed to start building RunBattle. Copy them into the appropriate files and customize as needed!
