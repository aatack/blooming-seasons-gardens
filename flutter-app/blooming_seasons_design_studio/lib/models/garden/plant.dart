import 'package:blooming_seasons_design_studio/models/inputs/validated.dart';
import 'package:flutter/material.dart' show Color, Colors, immutable;
import 'package:image/image.dart' show Image;

import '../structs/point.dart';
import 'instance.dart';

@immutable
class Plant implements Element {
  final ValidatedDouble diameter;

  final PlantType type;
  final PlantBorder border;
  final PlantImage image;

  const Plant({
    required this.diameter,
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
      "diameter": diameter.serialise(),
      "type": type.toString(),
      "border": _serialisePlantBorder(border),
      "image": _serialisePlantImage(image, images),
    };
  }

  static Plant blank() {
    return Plant(
      diameter: const ValidatedDouble("0.25"),
      type: PlantType.border,
      border: PlantBorder.blank(),
      image: PlantImage.blank(),
    );
  }
}

Plant deserialisePlant(dynamic plant, Map<int, Image> images) {
  final border = plant["border"];
  final image = plant["image"];

  return Plant(
    diameter: ValidatedDouble.deserialise(plant["diameter"]),
    type: PlantType.values
        .firstWhere((value) => value.toString() == plant["type"]),
    border: _deserialisePlantBorder(border),
    image: _deserialisePlantImage(image, images),
  );
}

enum PlantType { border, image }

@immutable
class PlantBorder {
  final ValidatedDouble thickness;
  final Color colour;

  const PlantBorder({required this.thickness, required this.colour});

  static PlantBorder blank() {
    return PlantBorder(
        thickness: const ValidatedDouble("1"), colour: Colors.yellow[300]!);
  }
}

dynamic _serialisePlantBorder(PlantBorder border) {
  return {
    "thickness": border.thickness.serialise(),
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
    thickness: ValidatedDouble.deserialise(border["thickness"]),
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
  final Point position;
  final ValidatedDouble scale;

  const PlantImage({
    required this.image,
    required this.position,
    required this.scale,
  });

  static PlantImage blank() {
    return PlantImage(
        image: null,
        position: Point.blank(),
        scale: const ValidatedDouble("0"));
  }
}

dynamic _serialisePlantImage(PlantImage image, Map<Image, int> images) {
  if (image.image != null && !images.containsKey(image)) {
    images[image.image!] = images.length;
  }

  return {
    "imageID": image.image == null ? null : images[image.image],
    "position": image.position.serialise(),
    "scale": image.scale.serialise(),
  };
}

PlantImage _deserialisePlantImage(dynamic image, Map<int, Image> images) {
  return PlantImage(
      image: image["imageID"] == null ? null : images[image["imageID"]]!,
      position: Point.deserialise(image["position"]),
      scale: ValidatedDouble.deserialise(image["scale"]));
}
