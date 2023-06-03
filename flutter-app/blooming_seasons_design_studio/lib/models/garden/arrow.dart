import 'package:flutter/material.dart' show immutable;
import 'package:image/image.dart' show Image;

import 'instance.dart';

@immutable
class Arrow implements BedElement {
  final double x;
  final double y;

  const Arrow({required this.x, required this.y});

  @override
  dynamic serialise(
    Map<int, dynamic> templates,
    Map<Image, int> images,
  ) {
    return {"x": x, "y": y};
  }
}

Arrow deserialiseArrow(dynamic arrow) {
  return Arrow(x: arrow["x"], y: arrow["y"]);
}
