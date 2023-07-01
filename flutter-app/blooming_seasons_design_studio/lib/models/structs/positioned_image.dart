import 'package:blooming_seasons_design_studio/models/inputs/validated.dart';
import 'package:blooming_seasons_design_studio/models/structs/point.dart';
import 'package:flutter/material.dart';

import '../../images.dart';

@immutable
class PositionedImage {
  final CachedImage? image;
  final Point position;
  final ValidatedDouble scale;

  const PositionedImage(
      {required this.image, required this.position, required this.scale});

  Map<String, dynamic> serialise() {
    return {
      "imageID": image?.id,
      "position": position.serialise(),
      "scale": scale.serialise(),
    };
  }

  static PositionedImage deserialise(
      dynamic image, Map<int, CachedImage> images) {
    return PositionedImage(
      image: image["imageID"] == null ? null : images[image["imageID"]]!,
      position: Point.deserialise(image["position"]),
      scale: ValidatedDouble.deserialise(image["scale"]),
    );
  }

  static PositionedImage blank() {
    return PositionedImage(
        image: null,
        position: Point.blank(),
        scale: const ValidatedDouble("0", minimum: 0));
  }
}
