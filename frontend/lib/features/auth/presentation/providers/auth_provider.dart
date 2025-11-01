import 'package:flutter/material.dart';
import '../../data/services/auth_service.dart';
import '../../data/models/user_model.dart';

class AuthProvider extends ChangeNotifier {
  final AuthService _authService;

  UserModel? _user;
  bool _isLoading = false;
  String? _errorMessage;

  AuthProvider(this._authService);

  UserModel? get user => _user;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  bool get isAuthenticated => _user != null;

  Future<bool> register({
    required String email,
    required String username,
    required String password,
    String? fullName,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final response = await _authService.register(
        email: email,
        username: username,
        password: password,
        fullName: fullName,
      );

      _user = UserModel.fromJson(response['user']);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> login({
    required String email,
    required String password,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final response = await _authService.login(
        email: email,
        password: password,
      );

      _user = UserModel.fromJson(response['user']);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> logout() async {
    await _authService.logout();
    _user = null;
    notifyListeners();
  }

  Future<void> checkAuthStatus() async {
    if (await _authService.isLoggedIn()) {
      try {
        _user = await _authService.getCurrentUser();
        notifyListeners();
      } catch (e) {
        await logout();
      }
    }
  }
}
