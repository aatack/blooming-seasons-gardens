import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../widgets/indicators/confirm.dart';

class ModalsState extends Cubit<List<Widget>> {
  ModalsState() : super([]);

  void add(Widget widget) {
    final List<Widget> updatedState = List.from(state);
    updatedState.add(widget);
    emit(updatedState);
  }

  void pop() {
    final List<Widget> updatedState = List.from(state);
    if (updatedState.isNotEmpty) {
      updatedState.removeLast();
    }
    emit(updatedState);
  }

  void clear() {
    emit([]);
  }

  void confirm({required String message, required void Function() action}) {
    add(
      Confirm(
        message: message,
        onCancel: () => pop(),
        onConfirm: () {
          pop();
          action();
        },
      ),
    );
  }
}
