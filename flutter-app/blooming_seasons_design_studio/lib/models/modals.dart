import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class ModalsState extends Cubit<List<Widget>> {
  ModalsState() : super([]);

  void append(Widget widget) {
    final List<Widget> updatedState = List.from(state);
    updatedState.add(widget);
    emit(updatedState);
  }

  void pop() {
    final List<Widget> updatedState = List.from(state);
    updatedState.removeLast();
    emit(updatedState);
  }

  void clear() {
    emit([]);
  }
}
