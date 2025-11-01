import 'package:dio/dio.dart';
import '../../../../core/utils/dio_client.dart';
import '../../../../core/constants/api_constants.dart';
import '../models/user_model.dart';

class AuthService {
  final DioClient _dioClient;

  AuthService(this._dioClient);

  Future<Map<String, dynamic>> register({
    required String email,
    required String username,
    required String password,
    String? fullName,
  }) async {
    try {
      final response = await _dioClient.dio.post(
        ApiConstants.register,
        data: {
          'email': email,
          'username': username,
          'password': password,
          if (fullName != null) 'full_name': fullName,
        },
      );

      final token = response.data['access_token'];
      await _dioClient.saveToken(token);

      return response.data;
    } on DioException catch (e) {
      throw Exception(e.response?.data['detail'] ?? 'Registration failed');
    }
  }

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _dioClient.dio.post(
        ApiConstants.login,
        data: {
          'email': email,
          'password': password,
        },
      );

      final token = response.data['access_token'];
      await _dioClient.saveToken(token);

      return response.data;
    } on DioException catch (e) {
      throw Exception(e.response?.data['detail'] ?? 'Login failed');
    }
  }

  Future<UserModel> getCurrentUser() async {
    try {
      final response = await _dioClient.dio.get(ApiConstants.me);
      return UserModel.fromJson(response.data);
    } on DioException catch (e) {
      throw Exception(e.response?.data['detail'] ?? 'Failed to get user');
    }
  }

  Future<void> logout() async {
    await _dioClient.deleteToken();
  }

  Future<bool> isLoggedIn() async {
    final token = await _dioClient.getToken();
    return token != null;
  }
}
