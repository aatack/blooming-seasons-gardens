import 'dart:collection';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../requests.dart';
import '../widgets/indicators/error.dart';
import 'garden/garden.dart';
import 'modals.dart';
import 'thunk.dart';

class SessionState extends Cubit<Session> {
  SessionState() : super(Session(Thunk.empty(), Thunk.empty(), const []));

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
      set: (result) => emit(Session(
        result,
        state.currentGarden,
        state.editHistory,
      )),
    );
  }

  void loadGarden(String name, ModalsState? modals) {
    Thunk.populate(
      get: () async {
        final garden = await queryBackend("/garden/get", body: {"name": name});
        return deserialiseGarden(garden);
      },
      set: (result) {
        result.handle(data: (data) {
          emit(Session(state.availableGardens, result, [data]));
        }, error: (error) {
          if (modals != null) {
            modals.add(ErrorIndicator(message: error.toString()));
            emit(Session(state.availableGardens, Thunk.empty(), const []));
          } else {
            emit(Session(state.availableGardens, result, const []));
          }
        }, loading: () {
          // TODO: potentially show the loading indicator in a modal, such
          //       that stateful widgets maintain their state while the
          //       garden loads (in case it fails to load properly)
          emit(Session(state.availableGardens, Thunk.loading(), const []));
        });
      },
    );
  }

  void createGarden(String name, ModalsState? modals) {
    Thunk.populate(
      get: () async {
        await queryBackend(
          "/garden/save",
          body: {"name": name, "content": serialiseGarden(Garden.blank(name))},
        );
        final garden = await queryBackend("/garden/get", body: {"name": name});
        return deserialiseGarden(garden);
      },
      set: (result) {
        result.handle(data: (data) {
          emit(Session(state.availableGardens, result, [data]));
        }, error: (error) {
          if (modals != null) {
            modals.add(ErrorIndicator(message: error.toString()));
            emit(Session(state.availableGardens, Thunk.empty(), const []));
          } else {
            emit(Session(state.availableGardens, result, const []));
          }
        }, loading: () {
          emit(Session(state.availableGardens, Thunk.loading(), const []));
        });
      },
    );
  }

  void deleteGarden(String name, ModalsState modals) {
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
              state.editHistory,
            ));
          },
        );
      },
    );
  }

  void renameGarden(String oldName, String newName, ModalsState modals) {
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
                state.editHistory,
              ),
            );
          },
        );
      },
    );
  }

  void exitGarden() {
    emit(Session(Thunk.empty(), Thunk.empty(), const []));
    // List of gardens may have changed in the meantime, so reload it
    loadGardens();
  }

  void editGarden(
    Garden Function(Garden) update, {
    bool addToHistory = true,
  }) {
    final oldGarden = state.currentGarden.unpack();

    if (oldGarden != null) {
      final newGarden = update(oldGarden);
      emit(Session(
        state.availableGardens,
        Thunk.data(newGarden),
        addToHistory ? [...state.editHistory, newGarden] : state.editHistory,
      ));
    }
  }
}

@immutable
class Session {
  final Thunk<UnmodifiableListView<String>> availableGardens;
  final Thunk<Garden> currentGarden;

  final List<Garden> _editHistory;
  UnmodifiableListView<Garden> get editHistory =>
      UnmodifiableListView(_editHistory);

  const Session(this.availableGardens, this.currentGarden, this._editHistory);
}
