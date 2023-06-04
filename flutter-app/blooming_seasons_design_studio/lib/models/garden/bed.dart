import 'dart:collection';

import 'package:image/image.dart' show Image;
import 'package:flutter/material.dart' show immutable;

import 'instance.dart';

@immutable
class Bed {
  final int id;

  final List<Instance<Element>> _elements;
  UnmodifiableListView<Instance<Element>> get elements =>
      UnmodifiableListView(_elements);

  final double x;
  final double y;

  final String name;

  const Bed(this._elements,
      {required this.id, required this.x, required this.y, required this.name});

  dynamic serialise(
    Map<int, dynamic> templates,
    Map<Image, int> images,
  ) {}
}

dynamic serialiseBed(
    Bed bed, Map<int, dynamic> templates, Map<Image, int> images) {
  return {
    "elements": bed.elements
        .map(
          (element) => serialiseInstance(element, templates, images),
        )
        .toList(),
    "x": bed.x,
    "y": bed.y,
    "name": bed.name,
  };
}

Bed deserialiseBed(Map<String, dynamic> bed, Map<int, Element> templates,
    Map<int, Image> images) {
  return Bed(
    bed["elements"].map((element) => deserialiseElement(element, images)),
    id: bed["id"],
    x: bed["x"],
    y: bed["y"],
    name: bed["name"],
  );
}
