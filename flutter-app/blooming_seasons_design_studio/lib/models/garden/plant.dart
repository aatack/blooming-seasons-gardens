import 'package:flutter/material.dart' show Color, immutable;
import 'package:image/image.dart' show Image;

import 'instance.dart';

@immutable
class Plant implements BedElement {
  final String name;

  final double size;

  final PlantType type;
  final PlantBorder? border;
  final PlantImage? image;

  const Plant(this.name, this.size, this.type, this.border, this.image);

  @override
  dynamic serialise(
    Map<int, dynamic> templates,
    Map<Image, int> images,
  ) {
    return {
      "name": name,
      "size": size,
      "type": type.toString(),
      "border": border ?? _serialiseBorder(border!),
      "image": image ?? _serialiseImage(image!, images),
    };
  }
}

enum PlantType { border, image }

@immutable
class PlantBorder {
  final double thickness;
  final Color colour;

  const PlantBorder(this.thickness, this.colour);
}

dynamic _serialiseBorder(PlantBorder border) {
  return {
    "thickness": border.thickness,
    "colour": {
      "red": border.colour.red,
      "green": border.colour.green,
      "blue": border.colour.blue,
      "alpha": border.colour.alpha,
    }
  };
}

@immutable
class PlantImage {
  final Image image;
  final double x;
  final double y;
  final double scale;

  const PlantImage(this.image, this.x, this.y, this.scale);
}

dynamic _serialiseImage(PlantImage image, Map<Image, int> images) {
  if (!images.containsKey(image)) {
    images[image.image] = images.length;
  }

  return {
    "image": images[image.image],
    "x": image.x,
    "y": image.y,
    "scale": image.scale,
  };
}
