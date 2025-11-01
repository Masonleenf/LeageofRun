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
