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
