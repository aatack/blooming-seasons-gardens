import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'garden.dart';
import 'thunk.dart';

class SessionState extends Cubit<Session> {
  SessionState() : super(Session(Thunk.empty(), Thunk.empty()));

  void loadAvailableGardens() {
    Thunk.populate(
      get: () async {
        await Future.delayed(const Duration(seconds: 2));
        return [""];
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
