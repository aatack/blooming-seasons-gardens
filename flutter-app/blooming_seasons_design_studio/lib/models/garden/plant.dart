import 'package:flutter/material.dart' show Color, immutable;
import 'package:image/image.dart' show Image;

import '../structs/point.dart';
import 'instance.dart';

@immutable
class Plant implements Element {
  final String name;

  final double size;

  final PlantType type;
  final PlantBorder border;
  final PlantImage image;

  const Plant({
    required this.name,
    required this.size,
    required this.type,
    required this.border,
    required this.image,
  });

  @override
  Map<String, dynamic> serialise(
    Map<int, dynamic> templates,
    Map<Image, int> images,
  ) {
    return {
      "elementType": "plant",
      "name": name,
      "size": size,
      "type": type.toString(),
      "border": _serialisePlantBorder(border),
      "image": _serialisePlantImage(image, images),
    };
  }
}

Plant deserialisePlant(dynamic plant, Map<int, Image> images) {
  final border = plant["border"];
  final image = plant["image"];

  return Plant(
    name: plant["name"],
    size: plant["size"],
    type: PlantType.values
        .firstWhere((value) => value.toString() == plant["type"]),
    border: _deserialisePlantBorder(border),
    image: _deserialisePlantImage(image, images),
  );
}

enum PlantType { border, image }

@immutable
class PlantBorder {
  final double thickness;
  final Color colour;

  const PlantBorder({required this.thickness, required this.colour});
}

dynamic _serialisePlantBorder(PlantBorder border) {
  return {
    "thickness": border.thickness,
    "colour": {
      "alpha": border.colour.alpha,
      "red": border.colour.red,
      "green": border.colour.green,
      "blue": border.colour.blue,
    }
  };
}

PlantBorder _deserialisePlantBorder(dynamic border) {
  final colour = border["colour"];

  return PlantBorder(
    thickness: border["thickness"],
    colour: Color.fromARGB(
      colour["alpha"],
      colour["red"],
      colour["green"],
      colour["blue"],
    ),
  );
}

@immutable
class PlantImage {
  final Image? image;
  final double x;
  final double y;
  final double scale;

  const PlantImage({
    required this.image,
    required this.x,
    required this.y,
    required this.scale,
  });

  static PlantImage blank() {
    return const PlantImage(image: null, x: 0, y: 0, scale: 1);
  }
}

dynamic _serialisePlantImage(PlantImage image, Map<Image, int> images) {
  if (image.image != null && !images.containsKey(image)) {
    images[image.image!] = images.length;
  }

  return {
    "imageID": image.image == null ? null : images[image.image],
    "x": image.x,
    "y": image.y,
    "scale": image.scale,
  };
}

PlantImage _deserialisePlantImage(dynamic image, Map<int, Image> images) {
  return PlantImage(
      image: image["imageID"] == null ? null : images[image["imageID"]]!,
      x: image["x"],
      y: image["y"],
      scale: image["scale"]);
}
