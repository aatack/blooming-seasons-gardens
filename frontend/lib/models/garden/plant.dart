import 'package:blooming_seasons_gardens/models/inputs/validated.dart';
import 'package:blooming_seasons_gardens/models/structs/positioned_image.dart';
import 'package:flutter/material.dart' show Color, Colors, immutable;

import '../../images.dart';
import 'instance.dart';

@immutable
class Plant implements Element {
  final ValidatedDouble diameter;

  final PlantType type;
  final PlantFill fill;
  final PositionedImage image;

  const Plant({
    required this.diameter,
    required this.type,
    required this.fill,
    required this.image,
  });

  @override
  Map<String, dynamic> serialise() {
    return {
      "elementType": "plant",
      "diameter": diameter.serialise(),
      "type": type.toString(),
      "fill": _serialisePlantFill(fill),
      "image": image.serialise(),
    };
  }

  static Plant blank() {
    return Plant(
      diameter: ValidatedDouble.initialise(0.25, minimum: 0),
      type: PlantType.fill,
      fill: PlantFill.blank(),
      image: PositionedImage.blank(),
    );
  }

  Plant withDiameter(ValidatedDouble newDiameter) {
    return Plant(diameter: newDiameter, type: type, fill: fill, image: image);
  }

  Plant withType(PlantType newType) {
    return Plant(diameter: diameter, type: newType, fill: fill, image: image);
  }

  Plant withFill(PlantFill newFill) {
    return Plant(diameter: diameter, type: type, fill: newFill, image: image);
  }

  Plant withImage(PositionedImage newImage) {
    return Plant(diameter: diameter, type: type, fill: fill, image: newImage);
  }
}

Plant deserialisePlant(dynamic plant, Map<int, CachedImage> images) {
  final fill = plant["fill"];
  final image = plant["image"];

  return Plant(
    diameter: ValidatedDouble.deserialise(plant["diameter"]),
    type: PlantType.values
        .firstWhere((value) => value.toString() == plant["type"]),
    fill: _deserialisePlantFill(fill),
    image: PositionedImage.deserialise(image, images),
  );
}

enum PlantType { fill, image }

@immutable
class PlantFill {
  final ValidatedDouble thickness;
  final Color colour;

  const PlantFill({required this.thickness, required this.colour});

  static PlantFill blank() {
    return PlantFill(
        thickness: ValidatedDouble.initialise(1, minimum: 0),
        colour: Colors.yellow[300]!);
  }
}

dynamic _serialisePlantFill(PlantFill fill) {
  return {
    "thickness": fill.thickness.serialise(),
    "colour": {
      "alpha": fill.colour.alpha,
      "red": fill.colour.red,
      "green": fill.colour.green,
      "blue": fill.colour.blue,
    }
  };
}

PlantFill _deserialisePlantFill(dynamic fill) {
  final colour = fill["colour"];

  return PlantFill(
    thickness: ValidatedDouble.deserialise(fill["thickness"]),
    colour: Color.fromARGB(
      colour["alpha"],
      colour["red"],
      colour["green"],
      colour["blue"],
    ),
  );
}
