import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'garden.dart';
import 'thunk.dart';

class SessionState extends Cubit<Session> {
  SessionState() : super(Session(Thunk.empty(), Thunk.empty()));

  void loadAvailableGardens() {
    Thunk.populate(
      get: () async {
        final response =
            await http.get(Uri.parse("http://localhost:3000/gardens/list"));

        if (response.statusCode == 200) {
          final jsonResponse = jsonDecode(response.body);
          if (jsonResponse is List<dynamic>) {
            return List<String>.from(jsonResponse);
          } else {
            throw const FormatException(
                "Response was not formatted as a list of strings");
          }
        } else {
          throw Exception("Could not load existing gardens");
        }
      },
      set: (data) => emit(Session(data, state.currentGarden)),
    );
  }

  void loadAvailableGarden(String name) {}

  void createAndLoadNewGarden(String name) {}
}

@immutable
class Session {
  final Thunk<List<String>> availableGardens;
  final Thunk<Garden> currentGarden;

  const Session(this.availableGardens, this.currentGarden);
}
