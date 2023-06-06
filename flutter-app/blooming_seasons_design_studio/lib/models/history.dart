import 'dart:collection';

import 'package:flutter/material.dart';

// NOTE: if this becomes a performance bottleneck, it can very easily be
//       replaced with a linked list

@immutable
class History<Data> {
  final List<Data> _past;
  UnmodifiableListView<Data> get past => UnmodifiableListView(_past);

  final Data present;

  final List<Data> _future;
  UnmodifiableListView<Data> get future => UnmodifiableListView(_future);

  const History(this._past, this.present, this._future);

  factory History.from(Data data) {
    return History(const [], data, const []);
  }
}
