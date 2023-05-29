import 'package:http/http.dart' as http;

Future<http.Response> queryBackend(
  String uri,
  dynamic body,
) {
  return http.post(Uri.parse("http://localhost:3000$uri"));
}
