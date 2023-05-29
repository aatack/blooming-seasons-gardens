import 'dart:collection';

import 'package:image/image.dart' show Image;
import 'package:flutter/material.dart' show Color, immutable;

@immutable
class Garden {
  final String name;

  final List<Instance<Bed>> _beds;
  UnmodifiableListView<Instance<Bed>> get beds => UnmodifiableListView(_beds);

  // Maps identifiers to a template associated with that identifier
  final Map<int, Element> _templates;
  UnmodifiableMapView<int, Element> get nursery =>
      UnmodifiableMapView(_templates);

  // The next available identifier for elements in the garden
  final int availableID;

  const Garden(this.name, this._beds, this._templates, this.availableID);

  factory Garden.blank(String name) {
    return Garden(name, const [], const {}, 1);
  }

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

abstract class Element {}

abstract class BedElement implements Element {}

@immutable
class Instance<E extends Element> {
  final int id;
  final double x;
  final double y;
  final E element;
  final int? template;

  const Instance(this.id, this.x, this.y, this.element, this.template);
}

@immutable
class Bed implements Element {
  final List<Instance<BedElement>> _elements;
  UnmodifiableListView<Instance<BedElement>> get elements =>
      UnmodifiableListView(_elements);

  const Bed(this._elements);
}

@immutable
class Plant implements BedElement {
  final String name;

  final double size;

  final PlantType plantType;
  final PlantBorder? border;
  final PlantImage? image;

  const Plant(this.name, this.size, this.plantType, this.border, this.image);
}

enum PlantType { border, image }

@immutable
class PlantBorder {
  final double thickness;
  final Color colour;

  const PlantBorder(this.thickness, this.colour);
}

@immutable
class PlantImage {
  final Image image;
  final double x;
  final double y;
  final double scale;

  const PlantImage(this.image, this.x, this.y, this.scale);
}

@immutable
class Label implements BedElement {
  final String text;
  final double size;

  const Label(this.text, this.size);
}

@immutable
class Arrow implements BedElement {
  final double x;
  final double y;

  const Arrow(this.x, this.y);
}
