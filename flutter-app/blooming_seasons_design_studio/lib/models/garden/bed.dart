import 'dart:collection';

import 'package:flutter/material.dart';

import 'instance.dart';

@immutable
class Bed implements GardenElement {
  final List<Instance<BedElement>> _elements;
  UnmodifiableListView<Instance<BedElement>> get elements =>
      UnmodifiableListView(_elements);

  const Bed(this._elements);
}

dynamic serialiseBed(Bed bed, Map<int, dynamic> templates) {
  throw UnimplementedError();
}
