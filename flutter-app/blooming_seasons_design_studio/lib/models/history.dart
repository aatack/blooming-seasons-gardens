import 'dart:collection';

import 'package:flutter/material.dart';

import 'garden/garden.dart';

@immutable
class GardenHistory {
  final List<Garden> _past;
  UnmodifiableListView<Garden> get past => UnmodifiableListView(_past);

  final Garden present;

  final List<Garden> _future;
  UnmodifiableListView<Garden> get future => UnmodifiableListView(_future);

  const GardenHistory(this._past, this.present, this._future);

  factory GardenHistory.from(Garden garden) {
    return GardenHistory(const [], garden, const []);
  }
}
