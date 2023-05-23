import 'dart:convert';

import 'package:blooming_seasons_design_studio/models/modals.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../widgets/indicators/error.dart';
import 'garden.dart';
import 'thunk.dart';

class SessionState extends Cubit<Session> {
  SessionState() : super(Session(Thunk.empty(), Thunk.empty()));

  void loadGardens() {
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
      set: (result) => emit(Session(result, state.currentGarden)),
    );
  }

  void loadGarden(String name, ModalsState? modals) {
    Thunk.populate(
      get: () async {
        try {
          final response = await http
              .get(Uri.parse("http://localhost:3000/gardens/get/$name"));

          if (response.statusCode == 200) {
            return Garden.blank(response.body);
          } else {
            throw "Error from server: ${response.body}";
          }
        } catch (error) {
          throw "Error from client: $error";
        }
      },
      set: (result) {
        result.handle(data: (data) {
          emit(Session(state.availableGardens, Thunk.data(data)));
        }, error: (error) {
          if (modals != null) {
            modals.add(ErrorIndicator(message: error.toString()));
            emit(Session(state.availableGardens, Thunk.empty()));
          } else {
            emit(Session(state.availableGardens, Thunk.error(error)));
          }
        }, loading: () {
          emit(Session(state.availableGardens, Thunk.loading()));
        });
      },
    );
  }

  void createAndLoadNewGarden(String name) {}
}

@immutable
class Session {
  final Thunk<List<String>> availableGardens;
  final Thunk<Garden> currentGarden;

  const Session(this.availableGardens, this.currentGarden);
}
