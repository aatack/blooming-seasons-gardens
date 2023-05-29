import 'dart:collection';

import 'package:blooming_seasons_design_studio/requests.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../widgets/indicators/error.dart';
import 'garden/garden.dart';
import 'modals.dart';
import 'thunk.dart';

class SessionState extends Cubit<Session> {
  SessionState() : super(Session(Thunk.empty(), Thunk.empty()));

  void loadGardens() {
    Thunk.populate(
      get: () async {
        final gardens = await queryBackend("/garden/list");
        if (gardens is List<dynamic>) {
          return UnmodifiableListView(List<String>.from(gardens));
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
          emit(Session(state.availableGardens, result));
        }, error: (error) {
          if (modals != null) {
            modals.add(ErrorIndicator(message: error.toString()));
            emit(Session(state.availableGardens, Thunk.empty()));
          } else {
            emit(Session(state.availableGardens, result));
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

  void createGarden(String name, ModalsState? modals) {
    Thunk.populate(
      get: () async {
        await queryBackend(
          "/garden/save",
          body: {"name": name, "content": Garden.blank(name).serialise()},
        );
        final garden = await queryBackend("/garden/get", body: {"name": name});
        return Garden.deserialise(garden);
      },
      set: (result) {
        result.handle(data: (data) {
          emit(Session(state.availableGardens, result));
        }, error: (error) {
          if (modals != null) {
            modals.add(ErrorIndicator(message: error.toString()));
            emit(Session(state.availableGardens, Thunk.empty()));
          } else {
            emit(Session(state.availableGardens, result));
          }
        }, loading: () {
          emit(Session(state.availableGardens, Thunk.loading()));
        });
      },
    );
  }

  void deleteGarden(String name, ModalsState modals) {
    final initialState = state.availableGardens;

    Thunk.populate(
      get: () async {
        return await queryBackend("/garden/delete", body: {"name": name});
      },
      set: (result) {
        result.handle(
          data: (data) {},
          error: (error) {
            modals
                .add(ErrorIndicator(message: "Failed to delete garden: $name"));
            emit(state);
          },
          loading: () {
            emit(Session(
              state.availableGardens.map(
                (gardens) => UnmodifiableListView(
                    gardens.where((element) => element != name)),
              ),
              state.currentGarden,
            ));
          },
        );
      },
    );
  }

  void renameGarden(String oldName, String newName, ModalsState modals) {
    final initialState = state.availableGardens;

    Thunk.populate(
      get: () async {
        return await queryBackend(
          "/garden/rename",
          body: {"old-name": oldName, "new-name": newName},
        );
      },
      set: (result) {
        result.handle(
          data: (data) {},
          error: (error) {
            modals.add(
                ErrorIndicator(message: "Failed to rename garden: $oldName"));
            emit(state);
          },
          loading: () {
            emit(
              Session(
                state.availableGardens.map(
                  (gardens) => UnmodifiableListView(
                    gardens.map(
                      (garden) => garden == oldName ? newName : garden,
                    ),
                  ),
                ),
                state.currentGarden,
              ),
            );
          },
        );
      },
    );
  }
}

@immutable
class Session {
  final Thunk<UnmodifiableListView<String>> availableGardens;
  final Thunk<Garden> currentGarden;

  const Session(this.availableGardens, this.currentGarden);
}
