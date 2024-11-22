import 'dart:collection';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../requests.dart';
import '../widgets/indicators/error.dart';
import 'garden/garden.dart';
import 'history.dart';
import 'modals.dart';
import 'selections.dart';
import 'thunk.dart';

class SessionState extends Cubit<Session> {
  SessionState()
      : super(Session(Thunk.empty(), Thunk.empty(), Selections.blank()));

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
      set: (result) => emit(Session(result, state.garden, state.selections)),
    );
  }

  void loadGarden(String name, ModalsState? modals) {
    Thunk.populate(
      get: () async {
        final garden = await queryBackend("/garden/get", body: {"name": name});
        return History.from(await deserialiseGarden(garden));
      },
      set: (result) {
        result.handle(data: (data) {
          emit(Session(state.gardens, result, Selections.blank()));
        }, error: (error) {
          if (modals != null) {
            modals.add(ErrorIndicator(message: error.toString()));
            emit(Session(state.gardens, Thunk.empty(), state.selections));
          } else {
            emit(Session(state.gardens, result, Selections.blank()));
          }
        }, loading: () {
          // TODO: potentially show the loading indicator in a modal, such
          //       that stateful widgets maintain their state while the
          //       garden loads (in case it fails to load properly)
          emit(Session(state.gardens, Thunk.loading(), state.selections));
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
        return History.from(await deserialiseGarden(garden));
      },
      set: (result) {
        result.handle(data: (data) {
          emit(Session(state.gardens, result, Selections.blank()));
        }, error: (error) {
          if (modals != null) {
            modals.add(ErrorIndicator(message: error.toString()));
            emit(Session(state.gardens, Thunk.empty(), state.selections));
          } else {
            emit(Session(state.gardens, result, Selections.blank()));
          }
        }, loading: () {
          emit(Session(state.gardens, Thunk.loading(), state.selections));
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
              state.selections,
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
                state.selections,
              ),
            );
          },
        );
      },
    );
  }

  void saveGarden() {
    state.garden.handle(
      data: (garden) {
        queryBackend(
          "/garden/save",
          body: {
            "name": garden.present.name,
            "content": serialiseGarden(garden.present),
          },
        );
      },
      error: (_) {},
      loading: () {},
    );
  }

  void exitGarden() {
    emit(Session(Thunk.empty(), Thunk.empty(), state.selections));
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
        state.selections,
      ),
    );
  }

  void undo() {
    emit(
      Session(state.gardens, state.garden.fmap((history) => history.back()),
          state.selections),
    );
  }

  void redo() {
    emit(
      Session(state.gardens, state.garden.fmap((history) => history.forward()),
          state.selections),
    );
  }

  void updateSelections(Selections Function(Selections) update) {
    emit(Session(state.gardens, state.garden, update(state.selections)));
  }
}

@immutable
class Session {
  final Thunk<UnmodifiableListView<String>> gardens;
  final Thunk<History<Garden>> garden;
  final Selections selections;

  const Session(this.gardens, this.garden, this.selections);
}
