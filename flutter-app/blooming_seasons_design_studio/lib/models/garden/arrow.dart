import 'package:blooming_seasons_design_studio/models/inputs/validated.dart';
import 'package:flutter/material.dart' show immutable;

import '../structs/point.dart';
import 'instance.dart';

@immutable
class Arrow implements Element {
  final Point source;
  final ValidatedDouble thickness;

  const Arrow({required this.source, required this.thickness});

  @override
  dynamic serialise(
    Map<int, dynamic> templates,
    Map<String, int> images,
  ) {
    return {
      "elementType": "arrow",
      "source": source.serialise(),
      "thickness": thickness.serialise(),
    };
  }

  Arrow withSource(Point newSource) {
    return Arrow(source: newSource, thickness: thickness);
  }

  Arrow withThickness(ValidatedDouble newThickness) {
    return Arrow(source: source, thickness: newThickness);
  }

  static Arrow blank() {
    return Arrow(source: Point.blank(), thickness: const ValidatedDouble("1"));
  }
}

Arrow deserialiseArrow(dynamic arrow) {
  return Arrow(
    source: Point.deserialise(arrow["source"]),
    thickness: ValidatedDouble.deserialise(arrow["thickness"]),
  );
}
