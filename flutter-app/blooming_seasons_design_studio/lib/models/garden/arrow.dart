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
  dynamic serialise() {
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
    return const Arrow(
        source: Point(ValidatedDouble("10"), ValidatedDouble("10")),
        thickness: ValidatedDouble("1"));
  }
}

Arrow deserialiseArrow(dynamic arrow) {
  return Arrow(
    source: Point.deserialise(arrow["source"]),
    thickness: ValidatedDouble.deserialise(arrow["thickness"]),
  );
}
