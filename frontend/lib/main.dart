import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/utils/dio_client.dart';
import 'features/auth/data/services/auth_service.dart';
import 'features/auth/presentation/providers/auth_provider.dart';
import 'features/auth/presentation/screens/login_screen.dart';
import 'features/auth/presentation/screens/register_screen.dart';
import 'features/home/presentation/screens/home_screen.dart';
import 'features/running/presentation/screens/running_screen.dart';
import 'features/battle/presentation/screens/battle_screen.dart';
import 'features/profile/presentation/screens/profile_screen.dart';

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
        initialRoute: '/login',
        routes: {
          '/login': (context) => const LoginScreen(),
          '/register': (context) => const RegisterScreen(),
          '/home': (context) => const HomeScreen(),
          '/running': (context) => const RunningScreen(),
          '/battle': (context) => const BattleScreen(),
          '/profile': (context) => const ProfileScreen(),
        },
      ),
    );
  }
}
