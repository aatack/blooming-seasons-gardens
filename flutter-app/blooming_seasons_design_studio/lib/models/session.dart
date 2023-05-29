
import 'package:blooming_seasons_design_studio/requests.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../widgets/indicators/error.dart';
import 'garden.dart';
import 'modals.dart';
import 'thunk.dart';

class SessionState extends Cubit<Session> {
  SessionState() : super(Session(Thunk.empty(), Thunk.empty()));

  void loadGardens() {
    Thunk.populate(
      get: () async {
        final gardens = await queryBackend("/garden/list");
        if (gardens is List<dynamic>) {
          return List<String>.from(gardens);
        } else {
          throw "Response was not formatted as a list of strings";
        }
      },
      set: (result) => emit(Session(result, state.currentGarden)),
    );
  }

  void loadGarden(String name, ModalsState? modals) {
    Thunk.populate(
      get: () async {
        final garden = await queryBackend("/garden/get", body: {"name": name});
        // TODO: actually parse the garden
        return Garden.blank(garden.toString());
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
          // TODO: potentially show the loading indicator in a modal, such
          //       that stateful widgets maintain their state while the
          //       garden loads (in case it fails to load properly)
          emit(Session(state.availableGardens, Thunk.loading()));
        });
      },
    );
  }

  void createAndLoadNewGarden(String name, ModalsState modals) {
    throw "Not implemented";
  }
}

@immutable
class Session {
  final Thunk<List<String>> availableGardens;
  final Thunk<Garden> currentGarden;

  const Session(this.availableGardens, this.currentGarden);
}
