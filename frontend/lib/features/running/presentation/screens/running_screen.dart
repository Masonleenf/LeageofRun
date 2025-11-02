import 'package:flutter/material.dart';
import 'dart:async';

class RunningScreen extends StatefulWidget {
  const RunningScreen({Key? key}) : super(key: key);

  @override
  State<RunningScreen> createState() => _RunningScreenState();
}

class _RunningScreenState extends State<RunningScreen> {
  bool _isRunning = false;
  bool _isPaused = false;

  // Running stats
  double _distance = 0.0; // km
  int _duration = 0; // seconds
  double _pace = 0.0; // min/km
  double _speed = 0.0; // km/h
  int _calories = 0;

  Timer? _timer;

  // Temporary: Simulate running data
  void _startRun() {
    setState(() {
      _isRunning = true;
      _isPaused = false;
    });

    // Start timer
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (!_isPaused) {
        setState(() {
          _duration++;

          // Simulate data (replace with actual GPS tracking)
          _distance += 0.003; // ~3 meters per second = 10.8 km/h

          if (_distance > 0 && _duration > 0) {
            _speed = (_distance / (_duration / 3600));
            _pace = (_duration / 60) / _distance;
            _calories = (_distance * 70).toInt(); // Simplified calculation
          }
        });
      }
    });
  }

  void _pauseRun() {
    setState(() {
      _isPaused = true;
    });
  }

  void _resumeRun() {
    setState(() {
      _isPaused = false;
    });
  }

  void _stopRun() {
    _timer?.cancel();

    // Show summary dialog
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        title: const Text('Run Summary'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildSummaryRow('Distance', '${_distance.toStringAsFixed(2)} km'),
            _buildSummaryRow('Duration', _formatDuration(_duration)),
            _buildSummaryRow('Pace', '${_pace.toStringAsFixed(2)} min/km'),
            _buildSummaryRow('Speed', '${_speed.toStringAsFixed(2)} km/h'),
            _buildSummaryRow('Calories', '$_calories kcal'),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              // Reset and go back
              setState(() {
                _isRunning = false;
                _isPaused = false;
                _distance = 0.0;
                _duration = 0;
                _pace = 0.0;
                _speed = 0.0;
                _calories = 0;
              });
              Navigator.pop(context);
            },
            child: const Text('Discard'),
          ),
          ElevatedButton(
            onPressed: () {
              // TODO: Save run to backend
              setState(() {
                _isRunning = false;
                _isPaused = false;
                _distance = 0.0;
                _duration = 0;
                _pace = 0.0;
                _speed = 0.0;
                _calories = 0;
              });
              Navigator.pop(context);
              Navigator.pop(context); // Go back to home

              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Run saved successfully!'),
                  backgroundColor: Colors.green,
                ),
              );
            },
            child: const Text('Save Run'),
          ),
        ],
      ),
    );
  }

  Widget _buildSummaryRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontWeight: FontWeight.w500)),
          Text(value, style: const TextStyle(fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  String _formatDuration(int seconds) {
    final hours = seconds ~/ 3600;
    final minutes = (seconds % 3600) ~/ 60;
    final secs = seconds % 60;

    if (hours > 0) {
      return '${hours.toString().padLeft(2, '0')}:${minutes.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
    } else {
      return '${minutes.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Running'),
        leading: _isRunning
            ? null
            : IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: () => Navigator.pop(context),
              ),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: [
              // Map placeholder
              Expanded(
                flex: 2,
                child: Container(
                  decoration: BoxDecoration(
                    color: Colors.grey[300],
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.map, size: 64, color: Colors.grey),
                        SizedBox(height: 8),
                        Text(
                          'Map View',
                          style: TextStyle(
                            fontSize: 18,
                            color: Colors.grey,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                        SizedBox(height: 4),
                        Text(
                          '(Google Maps will be shown here)',
                          style: TextStyle(fontSize: 12, color: Colors.grey),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 24),

              // Stats section
              Expanded(
                flex: 1,
                child: Column(
                  children: [
                    // Duration (main stat)
                    Text(
                      _formatDuration(_duration),
                      style: const TextStyle(
                        fontSize: 48,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Other stats
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        _buildStatColumn(
                          'Distance',
                          '${_distance.toStringAsFixed(2)}',
                          'km',
                        ),
                        _buildStatColumn(
                          'Pace',
                          _pace > 0 ? _pace.toStringAsFixed(2) : '--',
                          'min/km',
                        ),
                        _buildStatColumn(
                          'Speed',
                          _speed > 0 ? _speed.toStringAsFixed(1) : '--',
                          'km/h',
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              // Control buttons
              const SizedBox(height: 24),
              if (!_isRunning)
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _startRun,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 20),
                      backgroundColor: Colors.green,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: const Text(
                      'START RUN',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                )
              else
                Row(
                  children: [
                    Expanded(
                      child: ElevatedButton(
                        onPressed: _isPaused ? _resumeRun : _pauseRun,
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 20),
                          backgroundColor: _isPaused ? Colors.green : Colors.orange,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                        ),
                        child: Text(
                          _isPaused ? 'RESUME' : 'PAUSE',
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: ElevatedButton(
                        onPressed: _stopRun,
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 20),
                          backgroundColor: Colors.red,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                        ),
                        child: const Text(
                          'STOP',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatColumn(String label, String value, String unit) {
    return Column(
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 14,
            color: Colors.grey,
            fontWeight: FontWeight.w500,
          ),
        ),
        const SizedBox(height: 4),
        RichText(
          text: TextSpan(
            style: const TextStyle(color: Colors.black),
            children: [
              TextSpan(
                text: value,
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              TextSpan(
                text: ' $unit',
                style: const TextStyle(
                  fontSize: 14,
                  color: Colors.grey,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
