import 'dart:collection';

import 'package:flutter/material.dart' show immutable;

import '../../images.dart';
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

  late final Map<int, Instance> _instanceMap;
  UnmodifiableMapView<int, Instance> get instanceMap =>
      UnmodifiableMapView(_instanceMap);

  late final Set<int> _usedTemplates;
  UnmodifiableSetView<int> get usedTemplates =>
      UnmodifiableSetView(_usedTemplates);

  Bed(this._instances,
      {required this.id, required this.origin, required this.name}) {
    _instanceMap = Map.fromEntries(
        instances.map((instance) => MapEntry(instance.id, instance)));
    _usedTemplates = Set.from(instances
        .map((instance) => instance.templateId)
        .where((template) => template != null));
  }

  Bed rename(String newName) {
    return Bed(_instances, id: id, origin: origin, name: newName);
  }

  Bed updateInstances(Instance Function(Instance) update) {
    return Bed(_instances.map(update).toList(),
        id: id, origin: origin, name: name);
  }
}

dynamic serialiseBed(Bed bed) {
  return {
    "id": bed.id,
    "instances": bed.instances
        .map(
          (element) => serialiseInstance(element),
        )
        .toList(),
    "origin": bed.origin.serialise(),
    "name": bed.name,
  };
}

Bed deserialiseBed(Map<String, dynamic> bed, Map<int, CachedImage> images) {
  return Bed(
    (bed["instances"] as List<dynamic>)
        .map((instance) => deserialiseInstance(instance, images))
        .toList(),
    id: bed["id"],
    origin: Point.deserialise(bed["origin"]),
    name: bed["name"],
  );
}
