import 'dart:collection';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:image/image.dart' show Image;
import 'package:flutter/material.dart' show Color;

class GardenState extends Cubit<Garden?> {
  GardenState() : super(null);
}

class Garden {
  const Garden(this._beds, this._nursery, this.currentID);

  Garden.empty()
      : _beds = [],
        _nursery = [],
        currentID = 1;

  final List<Instance<Bed>> _beds;
  UnmodifiableListView<Instance<Bed>> get beds => UnmodifiableListView(_beds);

  final List<Template> _nursery;
  UnmodifiableListView<Template> get nursery => UnmodifiableListView(_nursery);

  final int currentID;

  Garden incrementID() {
    return Garden(_beds, _nursery, currentID + 1);
  }
}

class Instance<E> {
  const Instance(this.id, this.x, this.y, this.element);

  Instance.empty(Garden garden, E newElement)
      : id = garden.currentID,
        x = 0.0,
        y = 0.0,
        element = newElement;

  final int id;
  final double x;
  final double y;
  final E element;
}

class Template {
  const Template(this.id, this.plant);

  final int id;
  final Plant plant;
}

class Bed {
  const Bed(this._elements);

  final List<Instance> _elements;
  UnmodifiableListView<Instance> get elements =>
      UnmodifiableListView(_elements);
}

class Plant {
  const Plant(this.name, this.size, this.plantType, this.border, this.image);

  final String name;

  final double size;

  final PlantType plantType;
  final PlantBorder? border;
  final PlantImage? image;
}

enum PlantType { border, image }

class PlantBorder {
  const PlantBorder(this.thickness, this.colour);

  final double thickness;
  final Color colour;
}

class PlantImage {
  const PlantImage(this.image, this.x, this.y, this.scale);

  final Image image;
  final double x;
  final double y;
  final double scale;
}

class Label {
  const Label(this.text, this.size);

  final String text;
  final double size;
}

class Arrow {
  const Arrow(this.x, this.y);

  final double x;
  final double y;
}
