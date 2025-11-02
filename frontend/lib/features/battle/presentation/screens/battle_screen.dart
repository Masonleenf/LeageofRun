import 'package:flutter/material.dart';

class BattleScreen extends StatefulWidget {
  const BattleScreen({Key? key}) : super(key: key);

  @override
  State<BattleScreen> createState() => _BattleScreenState();
}

class _BattleScreenState extends State<BattleScreen> {
  bool _isSearching = false;
  bool _battleFound = false;
  Map<String, dynamic>? _opponent;

  final List<Map<String, dynamic>> _recentBattles = [
    {
      'opponent': 'SpeedRunner23',
      'result': 'Won',
      'distance': '5.0 km',
      'yourTime': '24:30',
      'opponentTime': '26:15',
      'eloChange': '+15',
      'date': '2 hours ago',
    },
    {
      'opponent': 'FastFeet99',
      'result': 'Lost',
      'distance': '3.0 km',
      'yourTime': '17:45',
      'opponentTime': '16:30',
      'eloChange': '-12',
      'date': 'Yesterday',
    },
  ];

  void _findMatch() {
    setState(() {
      _isSearching = true;
    });

    // Simulate matchmaking
    Future.delayed(const Duration(seconds: 2), () {
      setState(() {
        _isSearching = false;
        _battleFound = true;
        _opponent = {
          'username': 'RunnerX',
          'elo': 1540,
          'level': 'Gold',
          'totalRuns': 38,
          'winRate': 65,
        };
      });
    });
  }

  void _startBattle() {
    // Navigate to running screen with battle mode
    Navigator.pushNamed(context, '/running');
    setState(() {
      _battleFound = false;
      _opponent = null;
    });
  }

  void _cancelMatch() {
    setState(() {
      _battleFound = false;
      _opponent = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('1v1 Battle'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Battle info card
            _buildInfoCard(),
            const SizedBox(height: 24),

            // Matchmaking section
            if (!_battleFound) ...[
              _buildMatchmakingSection(),
            ] else ...[
              _buildOpponentFoundSection(),
            ],

            const SizedBox(height: 24),

            // Recent battles
            _buildRecentBattlesSection(),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoCard() {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const Icon(Icons.flash_on, size: 48, color: Colors.orange),
            const SizedBox(height: 12),
            const Text(
              '1v1 Battle Mode',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Compete against runners of similar skill level',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildInfoItem(Icons.people, 'Live 1v1'),
                _buildInfoItem(Icons.timer, '5 km'),
                _buildInfoItem(Icons.emoji_events, 'Win ELO'),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoItem(IconData icon, String text) {
    return Column(
      children: [
        Icon(icon, color: Colors.blue),
        const SizedBox(height: 4),
        Text(
          text,
          style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
        ),
      ],
    );
  }

  Widget _buildMatchmakingSection() {
    return Column(
      children: [
        const Text(
          'Find Your Opponent',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        if (_isSearching)
          Card(
            child: Padding(
              padding: const EdgeInsets.all(32),
              child: Column(
                children: const [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Finding opponent...'),
                ],
              ),
            ),
          )
        else
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _findMatch,
              icon: const Icon(Icons.search),
              label: const Text('Find Match'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 20),
                backgroundColor: Colors.orange,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
          ),
      ],
    );
  }

  Widget _buildOpponentFoundSection() {
    if (_opponent == null) return const SizedBox();

    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const Text(
              'Opponent Found!',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.green,
              ),
            ),
            const SizedBox(height: 20),

            // Opponent info
            const CircleAvatar(
              radius: 40,
              backgroundColor: Colors.blue,
              child: Icon(Icons.person, size: 40, color: Colors.white),
            ),
            const SizedBox(height: 12),
            Text(
              _opponent!['username'],
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: Colors.amber,
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                '${_opponent!['level']} League - ELO: ${_opponent!['elo']}',
                style: const TextStyle(
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Stats
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildOpponentStat('Runs', '${_opponent!['totalRuns']}'),
                _buildOpponentStat('Win Rate', '${_opponent!['winRate']}%'),
              ],
            ),

            const SizedBox(height: 24),

            // Action buttons
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: _cancelMatch,
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                    child: const Text('Cancel'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  flex: 2,
                  child: ElevatedButton(
                    onPressed: _startBattle,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      backgroundColor: Colors.green,
                    ),
                    child: const Text('Start Battle!'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildOpponentStat(String label, String value) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        Text(
          label,
          style: const TextStyle(
            fontSize: 12,
            color: Colors.grey,
          ),
        ),
      ],
    );
  }

  Widget _buildRecentBattlesSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Recent Battles',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 12),
        ..._recentBattles.map((battle) => _buildBattleCard(battle)).toList(),
      ],
    );
  }

  Widget _buildBattleCard(Map<String, dynamic> battle) {
    final bool isWon = battle['result'] == 'Won';

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    CircleAvatar(
                      backgroundColor: isWon ? Colors.green : Colors.red,
                      radius: 20,
                      child: Icon(
                        isWon ? Icons.emoji_events : Icons.close,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          battle['opponent'],
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                        Text(
                          battle['date'],
                          style: const TextStyle(
                            fontSize: 12,
                            color: Colors.grey,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: isWon
                        ? Colors.green.withOpacity(0.2)
                        : Colors.red.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    '${battle['eloChange']} ELO',
                    style: TextStyle(
                      color: isWon ? Colors.green : Colors.red,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildBattleStatItem('Distance', battle['distance']),
                _buildBattleStatItem('Your Time', battle['yourTime']),
                _buildBattleStatItem('Opp. Time', battle['opponentTime']),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBattleStatItem(String label, String value) {
    return Column(
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 12,
            color: Colors.grey,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }
}
