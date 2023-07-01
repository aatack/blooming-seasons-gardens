import 'package:blooming_seasons_design_studio/models/inputs/validated.dart';
import 'package:blooming_seasons_design_studio/models/structs/point.dart';
import 'package:flutter/material.dart';

@immutable
class PositionedImage {
  final String? image;
  final Point position;
  final ValidatedDouble scale;

  const PositionedImage(
      {required this.image, required this.position, required this.scale});

  Map<String, dynamic> serialise(Map<String, int> images) {
    if (image != null && !images.containsKey(image!)) {
      images[image!] = images.length;
    }

    return {
      "imageID": image == null ? null : images[image],
      "position": position.serialise(),
      "scale": scale.serialise(),
    };
  }

  static PositionedImage deserialise(dynamic image, Map<int, String> images) {
    return PositionedImage(
      image: image["imageID"] == null ? null : images[image["imageID"]]!,
      position: Point.deserialise(image["position"]),
      scale: ValidatedDouble.deserialise(image["scale"]),
    );
  }
}
