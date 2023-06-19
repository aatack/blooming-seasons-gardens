import 'dart:collection';

import 'package:image/image.dart' show Image;
import 'package:flutter/material.dart' show immutable;

import '../structs/point.dart';
import 'instance.dart';

@immutable
class Bed {
  final int id;

  final List<Instance> _instances;
  UnmodifiableListView<Instance> get instances =>
      UnmodifiableListView(_instances);

  final Point origin;

  final String name;

  const Bed(this._instances,
      {required this.id, required this.origin, required this.name});

  dynamic serialise(
    Map<int, dynamic> templates,
    Map<Image, int> images,
  ) {}

  Bed rename(String newName) {
    return Bed(_instances, id: id, origin: origin, name: newName);
  }
}

dynamic serialiseBed(
    Bed bed, Map<int, dynamic> templates, Map<Image, int> images) {
  return {
    "id": bed.id,
    "elements": bed.instances
        .map(
          (element) => serialiseInstance(element, templates, images),
        )
        .toList(),
    "origin": bed.origin.serialise(),
    "name": bed.name,
  };
}

Bed deserialiseBed(Map<String, dynamic> bed, Map<int, Element> templates,
    Map<int, Image> images) {
  return Bed(
    bed["elements"].map((element) => deserialiseElement(element, images)),
    id: bed["id"],
    origin: Point.deserialise(bed["origin"]),
    name: bed["name"],
  );
}
