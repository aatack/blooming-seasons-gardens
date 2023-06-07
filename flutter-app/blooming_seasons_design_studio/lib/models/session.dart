import 'dart:collection';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../requests.dart';
import '../widgets/indicators/error.dart';
import 'garden/garden.dart';
import 'history.dart';
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
      set: (result) => emit(Session(result, state.garden)),
    );
  }

  void loadGarden(String name, ModalsState? modals) {
    Thunk.populate(
      get: () async {
        final garden = await queryBackend("/garden/get", body: {"name": name});
        return History.from(deserialiseGarden(garden));
      },
      set: (result) {
        result.handle(data: (data) {
          emit(Session(state.gardens, result));
        }, error: (error) {
          if (modals != null) {
            modals.add(ErrorIndicator(message: error.toString()));
            emit(Session(state.gardens, Thunk.empty()));
          } else {
            emit(Session(state.gardens, result));
          }
        }, loading: () {
          // TODO: potentially show the loading indicator in a modal, such
          //       that stateful widgets maintain their state while the
          //       garden loads (in case it fails to load properly)
          emit(Session(state.gardens, Thunk.loading()));
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
        return History.from(deserialiseGarden(garden));
      },
      set: (result) {
        result.handle(data: (data) {
          emit(Session(state.gardens, result));
        }, error: (error) {
          if (modals != null) {
            modals.add(ErrorIndicator(message: error.toString()));
            emit(Session(state.gardens, Thunk.empty()));
          } else {
            emit(Session(state.gardens, result));
          }
        }, loading: () {
          emit(Session(state.gardens, Thunk.loading()));
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
              state.gardens.fmap(
                (gardens) => UnmodifiableListView(
                  gardens.where((element) => element != name),
                ),
              ),
              state.garden,
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
                state.gardens.fmap(
                  (gardens) => UnmodifiableListView(
                    gardens.map(
                      (garden) => garden == oldName ? newName : garden,
                    ),
                  ),
                ),
                state.garden,
              ),
            );
          },
        );
      },
    );
  }

  void exitGarden() {
    emit(Session(Thunk.empty(), Thunk.empty()));
    // List of gardens may have changed in the meantime, so reload it
    loadGardens();
  }

  void editGarden(Garden Function(Garden) update, {bool transient = false}) {
    emit(
      Session(
        state.gardens,
        state.garden.fmap(
          (history) {
            return history.commit(
              update(history.present),
              transient: transient,
            );
          },
        ),
      ),
    );
  }

  void undo() {
    emit(
      Session(state.gardens, state.garden.fmap((history) => history.back())),
    );
  }

  void redo() {
    emit(
      Session(state.gardens, state.garden.fmap((history) => history.forward())),
    );
  }
}

@immutable
class Session {
  final Thunk<UnmodifiableListView<String>> gardens;
  final Thunk<History<Garden>> garden;

  const Session(this.gardens, this.garden);
}
