import 'package:flutter/material.dart';

import '../../models/structs/point.dart';
import 'form_layout.dart';
import 'text.dart';

class PointInput extends StatelessWidget {
  final Point point;
  final void Function(Point, bool) onChange;

  const PointInput({super.key, required this.point, required this.onChange});

  @override
  Widget build(BuildContext context) {
    return FormLayout(
      children: [
        FormLayoutItem(
          label: const Text("Horizontal"),
          child: validatedTextInput(
            point.x,
            (newValue, transient) {
              onChange(Point(point.x.set(newValue), point.y), transient);
            },
          ),
        ),
        FormLayoutItem(
          label: const Text("Vertical"),
          child: validatedTextInput(
            point.y,
            (newValue, transient) {
              onChange(Point(point.x, point.y.set(newValue)), transient);
            },
          ),
        )
      ],
    );
  }
}
