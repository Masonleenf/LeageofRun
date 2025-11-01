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
