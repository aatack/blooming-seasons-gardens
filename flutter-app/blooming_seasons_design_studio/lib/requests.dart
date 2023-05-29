import 'dart:convert';

import 'package:http/http.dart' as http;

Future<dynamic> queryBackend(String uri, {dynamic body}) async {
  final response = await http.post(
    Uri.parse("http://localhost:3000$uri"),
    body: jsonEncode(body),
  );

  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw response.body;
  }
}
