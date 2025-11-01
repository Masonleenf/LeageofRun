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
