import 'dart:collection';
import 'dart:ffi';
import 'package:image/image.dart' as img;

import 'package:flutter/material.dart';

class Garden {
  const Garden(this._beds, this._nursery);

  final List<Positioned<Bed>> _beds;
  UnmodifiableListView<Positioned<Bed>> get beds => UnmodifiableListView(_beds);

  final List<Template> _nursery;
  UnmodifiableListView<Template> get nursery => UnmodifiableListView(_nursery);
}

class Positioned<T> {
  const Positioned(this.id, this.x, this.y, this.element);

  final Int id;
  final Float x;
  final Float y;
  final T element;
}

class Template {
  const Template(this.id, this.plant);

  final Int id;
  final Plant plant;
}

class Bed {
  const Bed(this._elements);

  final List<Positioned> _elements;
  UnmodifiableListView<Positioned> get elements =>
      UnmodifiableListView(_elements);
}

class Plant {
  const Plant(this.name, this.size, this.plantType, this.border, this.image);

  final String name;

  final Float size;

  final PlantType plantType;
  final PlantBorder? border;
  final PlantImage? image;
}

enum PlantType { border, image }

class PlantBorder {
  const PlantBorder(this.thickness, this.colour);

  final Float thickness;
  final Color colour;
}

class PlantImage {
  const PlantImage(this.image, this.x, this.y, this.scale);

  final img.Image image;
  final Float x;
  final Float y;
  final Float scale;
}

class Label {
  const Label(this.text, this.size);

  final String text;
  final Float size;
}

class Arrow {
  const Arrow(this.x, this.y);

  final Float x;
  final Float y;
}
