class RunModel {
  final String id;
  final String userId;
  final double distanceKm;
  final int durationSeconds;
  final double avgPace;
  final double avgSpeed;
  final double caloriesBurned;
  final DateTime startedAt;
  final DateTime completedAt;
  final String source;

  RunModel({
    required this.id,
    required this.userId,
    required this.distanceKm,
    required this.durationSeconds,
    required this.avgPace,
    required this.avgSpeed,
    required this.caloriesBurned,
    required this.startedAt,
    required this.completedAt,
    required this.source,
  });

  factory RunModel.fromJson(Map<String, dynamic> json) {
    return RunModel(
      id: json['id'],
      userId: json['user_id'],
      distanceKm: (json['distance_km'] ?? 0.0).toDouble(),
      durationSeconds: json['duration_seconds'] ?? 0,
      avgPace: (json['avg_pace'] ?? 0.0).toDouble(),
      avgSpeed: (json['avg_speed'] ?? 0.0).toDouble(),
      caloriesBurned: (json['calories_burned'] ?? 0.0).toDouble(),
      startedAt: DateTime.parse(json['started_at']),
      completedAt: DateTime.parse(json['completed_at']),
      source: json['source'] ?? 'app',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'distance_km': distanceKm,
      'duration_seconds': durationSeconds,
      'avg_pace': avgPace,
      'avg_speed': avgSpeed,
      'calories_burned': caloriesBurned,
      'started_at': startedAt.toIso8601String(),
      'completed_at': completedAt.toIso8601String(),
      'source': source,
    };
  }
}
