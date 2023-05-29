import 'package:flutter/material.dart' show Color, immutable;
import 'package:image/image.dart' show Image;

import 'instance.dart';

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
