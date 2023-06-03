import 'dart:collection';
import 'dart:convert';

import 'package:flutter/material.dart' show immutable;
import 'package:image/image.dart' show Image;

import 'bed.dart';
import 'instance.dart';

@immutable
class Garden {
  final String name;

  final List<Instance<Bed>> _beds;
  UnmodifiableListView<Instance<Bed>> get beds => UnmodifiableListView(_beds);

  // Maps identifiers to a template associated with that identifier
  final Map<int, BedElement> _templates;
  UnmodifiableMapView<int, BedElement> get templates =>
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
    "templates":
        templates.map((id, template) => MapEntry(id.toString(), template)),
    "availableID": garden.availableID,
    "images": images.map((image, id) => MapEntry(id, _serialiseImage(image))),
  };
}

/// Produce a garden object from its JSON representation.
///
/// The format of the passed object should mirror that of the return format
/// of the `serialise` function.
Garden deserialiseGarden(dynamic garden) {
  final images = Map<int, Image>.from(
    garden["images"].map(
      (id, image) => MapEntry(id, _deserialiseImage(image)),
    ),
  );

  final templates = Map<int, BedElement>.from(
    garden["templates"].map(
      (id, template) => MapEntry(
        int.parse(id),
        deserialiseBedElement(
          template,
          images,
        ),
      ),
    ),
  );

  return Garden(garden["name"], [], templates, garden["availableID"]);
}

dynamic _serialiseImage(Image image) {
  return {
    "data": base64.encode(image.getBytes()),
    "width": image.width,
    "height": image.height,
  };
}

Image _deserialiseImage(dynamic image) {
  return Image.fromBytes(
    width: image["width"],
    height: image["height"],
    bytes: base64.decode(image["data"]).buffer,
  );
}
