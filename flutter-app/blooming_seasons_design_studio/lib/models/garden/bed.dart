import 'dart:collection';

import 'package:image/image.dart' show Image;
import 'package:flutter/material.dart' show immutable;

import 'instance.dart';

@immutable
class Bed implements GardenElement {
  final List<Instance<BedElement>> _elements;
  UnmodifiableListView<Instance<BedElement>> get elements =>
      UnmodifiableListView(_elements);

  const Bed(this._elements);

  @override
  dynamic serialise(
    Map<int, dynamic> templates,
    Map<Image, int> images,
  ) {
    throw UnimplementedError();
  }
}
