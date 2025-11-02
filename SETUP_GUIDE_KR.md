# 🚀 RunBattle 설정 가이드

이 문서는 RunBattle 앱을 실행하기 위해 필요한 외부 서비스와 설정 방법을 안내합니다.

---

## 📋 필요한 외부 서비스 목록

### 1. PostgreSQL 데이터베이스

**용도**: 사용자, 러닝 기록, 배틀, 크루 데이터 저장

**설치 방법**:

#### 옵션 A: 로컬 설치
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS (Homebrew)
brew install postgresql

# 서비스 시작
sudo service postgresql start  # Linux
brew services start postgresql  # macOS

# 데이터베이스 및 사용자 생성
sudo -u postgres psql
```

PostgreSQL 콘솔에서:
```sql
CREATE DATABASE runbattle;
CREATE USER runbattle WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE runbattle TO runbattle;
\q
```

#### 옵션 B: 클라우드 호스팅

**추천 서비스**:
- [Supabase](https://supabase.com) - 무료 티어 제공, PostgreSQL 호스팅
- [Neon](https://neon.tech) - 서버리스 PostgreSQL, 무료 티어
- [Railway](https://railway.app) - PostgreSQL 무료 티어
- [ElephantSQL](https://www.elephantsql.com) - PostgreSQL 전용, 무료 티어

**Supabase 사용 예시**:
1. https://supabase.com 접속 및 가입
2. "New Project" 클릭
3. 프로젝트 이름, 비밀번호, 지역 설정
4. Settings > Database에서 Connection String 복사
5. 형식: `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres`

**DATABASE_URL 설정**:
```env
DATABASE_URL=postgresql://runbattle:password@localhost:5432/runbattle
# 또는 클라우드
DATABASE_URL=postgresql://postgres:your_password@db.xxx.supabase.co:5432/postgres
```

---

### 2. Redis (선택사항 - 실시간 배틀용)

**용도**: 실시간 배틀 데이터 캐싱, 세션 관리

**설치 방법**:

#### 로컬 설치
```bash
# Ubuntu/Debian
sudo apt install redis-server

# macOS
brew install redis

# 서비스 시작
sudo service redis-server start  # Linux
brew services start redis  # macOS
```

#### 클라우드 호스팅
- [Redis Cloud](https://redis.com/cloud/) - 30MB 무료 티어
- [Upstash](https://upstash.com) - 서버리스 Redis, 무료 티어
- [Railway](https://railway.app) - Redis 무료 티어

**REDIS_URL 설정**:
```env
REDIS_URL=redis://localhost:6379/0
# 또는 클라우드
REDIS_URL=redis://default:password@redis-12345.upstash.io:6379
```

---

### 3. Google Maps API

**용도**: 러닝 경로 지도 표시, GPS 추적

**설정 방법**:

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성
3. "APIs & Services" > "Library"로 이동
4. 다음 API 활성화:
   - Maps SDK for Android
   - Maps SDK for iOS
   - Geolocation API
   - Places API (선택사항)
5. "Credentials" > "Create Credentials" > "API Key"
6. API 키 제한 설정 (보안 강화):
   - Android: 앱 패키지명과 SHA-1 지문 추가
   - iOS: Bundle ID 추가

**비용**:
- 월 $200 무료 크레딧 제공
- 지도 로드: 1,000회당 $2
- 일반 사용으로는 무료 크레딧 내 충분

**Backend 설정** (backend/.env):
```env
GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Frontend 설정**:

Android (frontend/android/app/src/main/AndroidManifest.xml):
```xml
<application>
    <meta-data
        android:name="com.google.android.geo.API_KEY"
        android:value="YOUR_API_KEY_HERE"/>
</application>
```

iOS (frontend/ios/Runner/AppDelegate.swift):
```swift
import GoogleMaps

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    GMSServices.provideAPIKey("YOUR_API_KEY_HERE")
    GeneratedPluginRegistrant.register(with: self)
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}
```

---

### 4. Google OAuth (구글 로그인)

**용도**: 구글 계정으로 로그인

**설정 방법**:

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. "APIs & Services" > "Credentials"
3. "Create Credentials" > "OAuth 2.0 Client ID"
4. 애플리케이션 유형:
   - Android: 패키지명과 SHA-1 지문
   - iOS: Bundle ID
   - Web: 승인된 리디렉션 URI

**Android SHA-1 지문 얻기**:
```bash
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
```

**필요한 정보**:
- Client ID (Android)
- Client ID (iOS)
- Client ID (Web)

**Frontend 패키지 추가** (pubspec.yaml):
```yaml
dependencies:
  google_sign_in: ^6.2.1
```

**Backend 설정** (.env):
```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

---

### 5. Strava API (선택사항)

**용도**: Strava 러닝 데이터 가져오기

**설정 방법**:

1. [Strava Developers](https://developers.strava.com) 접속
2. "Create & Manage Your App" 클릭
3. 애플리케이션 정보 입력:
   - Application Name: RunBattle
   - Website: 앱 웹사이트 (없으면 localhost)
   - Authorization Callback Domain: 백엔드 URL
4. Client ID와 Client Secret 발급

**Backend 설정** (.env):
```env
STRAVA_CLIENT_ID=your_strava_client_id
STRAVA_CLIENT_SECRET=your_strava_client_secret
STRAVA_REDIRECT_URI=http://localhost:8000/api/v1/integrations/strava/callback
```

---

### 6. Firebase (선택사항 - 푸시 알림용)

**용도**: 배틀 시작, 결과 등 푸시 알림

**설정 방법**:

1. [Firebase Console](https://console.firebase.google.com) 접속
2. "프로젝트 추가" 클릭
3. Android 앱 추가:
   - 패키지명 입력
   - google-services.json 다운로드
   - frontend/android/app/에 복사
4. iOS 앱 추가:
   - Bundle ID 입력
   - GoogleService-Info.plist 다운로드
   - frontend/ios/Runner/에 복사

**Backend 설정**:
1. Firebase 콘솔 > 프로젝트 설정 > 서비스 계정
2. "새 비공개 키 생성" 클릭
3. JSON 파일 다운로드
4. backend/firebase-credentials.json으로 저장

```env
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

---

## 🔧 전체 환경 변수 설정

### Backend (.env)

backend/.env 파일 생성:

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

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Strava Integration (Optional)
STRAVA_CLIENT_ID=your-strava-client-id
STRAVA_CLIENT_SECRET=your-strava-client-secret
STRAVA_REDIRECT_URI=http://localhost:8000/api/v1/integrations/strava/callback

# Firebase (Optional)
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]

# App
DEBUG=True
APP_NAME=RunBattle
APP_VERSION=1.0.0
```

**SECRET_KEY 생성**:
```bash
openssl rand -hex 32
```

### Frontend

frontend/lib/core/constants/api_constants.dart 수정:

```dart
class ApiConstants {
  // 로컬 개발
  static const String baseUrl = 'http://localhost:8000';

  // 또는 실제 서버 (배포 시)
  // static const String baseUrl = 'https://api.runbattle.com';

  static const String apiVersion = '/api/v1';
  // ... 나머지 코드
}
```

---

## 📦 설치 및 실행

### Backend

```bash
cd backend

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# .env 파일 설정 (위 내용 참고)
nano .env

# 데이터베이스 테이블 생성
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# 서버 실행
uvicorn app.main:app --reload
```

서버가 http://localhost:8000 에서 실행됩니다.
API 문서: http://localhost:8000/docs

### Frontend

```bash
cd frontend

# 의존성 설치
flutter pub get

# Android 실행
flutter run

# 또는 특정 디바이스
flutter devices  # 사용 가능한 디바이스 확인
flutter run -d <device-id>
```

---

## 🐳 Docker로 간편 실행 (선택사항)

Docker Compose를 사용하면 PostgreSQL과 Redis가 자동으로 설정됩니다:

```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down
```

---

## ⚠️ 주의사항

### 개발 환경

1. **API 키 보안**:
   - .env 파일은 절대 Git에 커밋하지 마세요
   - .gitignore에 .env 추가 확인

2. **CORS 설정**:
   - 개발 시: localhost 허용
   - 프로덕션: 실제 도메인만 허용

3. **데이터베이스 마이그레이션**:
   - 스키마 변경 시 데이터베이스 백업
   - Alembic 사용 (설정 예정)

### 프로덕션 배포

1. **환경 변수**:
   - DEBUG=False 설정
   - 강력한 SECRET_KEY 사용
   - CORS_ORIGINS 제한

2. **HTTPS 필수**:
   - 모든 API 통신 HTTPS
   - Google OAuth 리디렉션 HTTPS

3. **데이터베이스**:
   - 정기 백업 설정
   - 연결 풀링 최적화

---

## 📞 문제 해결

### 자주 발생하는 문제

1. **데이터베이스 연결 실패**
   ```
   Error: could not connect to server
   ```
   - PostgreSQL 서비스 실행 확인
   - DATABASE_URL 형식 확인
   - 방화벽 설정 확인

2. **Google Maps 표시 안됨**
   - API 키 확인
   - 청구 계정 활성화 확인
   - API 제한 설정 확인

3. **앱 빌드 실패**
   ```bash
   flutter clean
   flutter pub get
   flutter run
   ```

---

## 🎯 최소 요구사항으로 시작하기

처음 시작할 때는 다음만 있으면 됩니다:

**필수**:
1. PostgreSQL (로컬 또는 Supabase)
2. Google Maps API (무료)

**선택사항 (나중에 추가)**:
- Redis (실시간 배틀용)
- Google OAuth (로그인 편의성)
- Strava API (데이터 가져오기)
- Firebase (푸시 알림)

---

## 📚 추가 리소스

- [FastAPI 공식 문서](https://fastapi.tiangolo.com)
- [Flutter 공식 문서](https://docs.flutter.dev)
- [PostgreSQL 튜토리얼](https://www.postgresql.org/docs/)
- [Google Maps Platform](https://developers.google.com/maps/documentation)

---

**Happy Running! 🏃‍♂️💨**
