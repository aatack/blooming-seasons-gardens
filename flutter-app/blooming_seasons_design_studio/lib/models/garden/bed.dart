import 'dart:collection';

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

  Bed rename(String newName) {
    return Bed(_instances, id: id, origin: origin, name: newName);
  }
}

dynamic serialiseBed(
    Bed bed, Map<int, dynamic> templates, Map<String, int> images) {
  return {
    "id": bed.id,
    "instances": bed.instances
        .map(
          (element) => serialiseInstance(element, templates, images),
        )
        .toList(),
    "origin": bed.origin.serialise(),
    "name": bed.name,
  };
}

Bed deserialiseBed(Map<String, dynamic> bed, Map<int, Element> templates,
    Map<int, String> images) {
  return Bed(
    (bed["instances"] as List<dynamic>)
        .map((instance) => deserialiseInstance(instance, templates, images))
        .toList(),
    id: bed["id"],
    origin: Point.deserialise(bed["origin"]),
    name: bed["name"],
  );
}
