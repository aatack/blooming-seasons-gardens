import 'package:flutter/material.dart';

import '../inputs/validated.dart';

@immutable
class Point {
  final ValidatedDouble x;
  final ValidatedDouble y;

  const Point(this.x, this.y);

  Map<String, dynamic> serialise() {
    return {"x": x.serialise(), "y": y.serialise()};
  }

  static Point deserialise(Map<String, dynamic> point) {
    return Point(
      ValidatedDouble.deserialise(point["x"]),
      ValidatedDouble.deserialise(point["y"]),
    );
  }

  static Point blank() {
    return Point(ValidatedDouble.initialise(0), ValidatedDouble.initialise(0));
  }

  Offset get offset => Offset(x.output, y.output);
}
