import 'dart:collection';

import 'package:image/image.dart' show Image;
import 'package:flutter/material.dart' show Color, immutable;

@immutable
class Garden {
  const Garden(this.name, this._beds, this._templates, this.availableID);

  factory Garden.blank(String name) {
    return Garden(name, const [], const {}, 1);
  }

  final String name;

  final List<Instance<Bed>> _beds;
  UnmodifiableListView<Instance<Bed>> get beds => UnmodifiableListView(_beds);

  // Maps identifiers to a template associated with that identifier
  final Map<int, Template> _templates;
  UnmodifiableMapView<int, Template> get nursery =>
      UnmodifiableMapView(_templates);

  // The next available identifier for elements in the garden
  final int availableID;

  /// Return a JSON-compatible representation of the garden.
  dynamic serialise() {
    return "Garden.serialise not yet implemented";
  }

  /// Produce a garden object from its JSON representation.
  ///
  /// The format of the passed object should mirror that of the return format
  /// of the `serialise` function.
  factory Garden.deserialise(dynamic garden) {
    return Garden.blank(garden.toString());
  }
}

@immutable
class Template<Element> {
  const Template(this.id, this.element);

  final int id;
  final Element element;
}

@immutable
class Instance<Element> {
  const Instance(this.id, this.x, this.y, this.element);

  Instance.blank(Garden garden, Element newElement)
      : id = garden.availableID,
        x = 0.0,
        y = 0.0,
        element = newElement;

  final int id;
  final double x;
  final double y;
  final Element element;
}

@immutable
class Bed {
  const Bed(this._elements);

  final List<Instance> _elements;
  UnmodifiableListView<Instance> get elements =>
      UnmodifiableListView(_elements);
}

@immutable
class Plant {
  const Plant(this.name, this.size, this.plantType, this.border, this.image);

  final String name;

  final double size;

  final PlantType plantType;
  final PlantBorder? border;
  final PlantImage? image;
}

enum PlantType { border, image }

@immutable
class PlantBorder {
  const PlantBorder(this.thickness, this.colour);

  final double thickness;
  final Color colour;
}

@immutable
class PlantImage {
  const PlantImage(this.image, this.x, this.y, this.scale);

  final Image image;
  final double x;
  final double y;
  final double scale;
}

@immutable
class Label {
  const Label(this.text, this.size);

  final String text;
  final double size;
}

@immutable
class Arrow {
  const Arrow(this.x, this.y);

  final double x;
  final double y;
}
