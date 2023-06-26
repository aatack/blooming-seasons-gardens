import 'package:flutter/material.dart';

import '../../models/structs/point.dart';
import 'form_layout.dart';
import 'text.dart';

List<FormLayoutItem> pointInput({
  String? label,
  required Point point,
  required void Function(Point, bool) setPoint,
}) {
  return [
    if (label != null) FormLayoutItem(label: Text(label)),
    FormLayoutItem(
      label: const Text("Horizontal"),
      child: validatedTextInput(
        point.x,
        (newValue, transient) {
          setPoint(Point(point.x.set(newValue), point.y), transient);
        },
      ),
    ),
    FormLayoutItem(
      label: const Text("Vertical"),
      child: validatedTextInput(
        point.y,
        (newValue, transient) {
          setPoint(Point(point.x, point.y.set(newValue)), transient);
        },
      ),
    )
  ];
}
