import 'dart:collection';

import 'package:flutter/material.dart' show immutable, Image;

import 'bed.dart';
import 'instance.dart';

@immutable
class Garden {
  final String name;

  final List<Instance<Bed>> _beds;
  UnmodifiableListView<Instance<Bed>> get beds => UnmodifiableListView(_beds);

  // Maps identifiers to a template associated with that identifier
  final Map<int, GardenElement> _templates;
  UnmodifiableMapView<int, GardenElement> get nursery =>
      UnmodifiableMapView(_templates);

  // The next available identifier for elements in the garden
  final int availableID;

  const Garden(this.name, this._beds, this._templates, this.availableID);

  factory Garden.blank(String name) {
    return Garden(name, const [], const {}, 0);
  }
}

/// Return a JSON-compatible representation of the garden.
dynamic serialiseGarden(Garden garden) {
  final Map<int, dynamic> templates = {};
  final Map<Image, int> images = {};

  final List<dynamic> beds = garden.beds
      .map((bed) => serialiseInstance(bed, templates, images))
      .toList();

  return {
    "name": garden.name,
    "beds": beds,
    "templates": templates
        .map((id, template) => MapEntry(id, {...template, "id": id}))
        .values
        .toList(),
    "availableID": garden.availableID,
    "images": images.map((image, id) => MapEntry(id, _serialiseImage(image))),
  };
}

/// Produce a garden object from its JSON representation.
///
/// The format of the passed object should mirror that of the return format
/// of the `serialise` function.
Garden deserialiseGarden(dynamic garden) {
  return Garden.blank(garden.toString());
}

dynamic _serialiseImage(Image image) {
  throw UnimplementedError();
}

Image _deserialiseImage(dynamic image) {
  throw UnimplementedError();
}
