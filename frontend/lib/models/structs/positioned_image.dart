import 'package:blooming_seasons_gardens/models/inputs/validated.dart';
import 'package:blooming_seasons_gardens/models/structs/point.dart';
import 'package:blooming_seasons_gardens/widgets/top_down.dart';
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
      "imageId": image?.id,
      "position": position.serialise(),
      "scale": scale.serialise(),
    };
  }

  static PositionedImage deserialise(
      dynamic image, Map<int, CachedImage> images) {
    return PositionedImage(
      image: image["imageId"] == null ? null : images[image["imageId"]]!,
      position: Point.deserialise(image["position"]),
      scale: ValidatedDouble.deserialise(image["scale"]),
    );
  }

  static PositionedImage blank() {
    return PositionedImage(
        image: null,
        position: Point.blank(),
        scale: ValidatedDouble.initialise(1, minimum: 0));
  }
}

class PositionedImagePainter extends Painter {
  final PositionedImage image;

  PositionedImagePainter(this.image);

  @override
  void paint(Canvas canvas) {
    if (image.image != null) {
      canvas.save();
      canvas.translate(image.position.x.output, image.position.y.output);
      canvas.scale(image.scale.output);

      canvas.drawImage(image.image!.image, Offset.zero, Paint());

      canvas.restore();
    }
  }
}
