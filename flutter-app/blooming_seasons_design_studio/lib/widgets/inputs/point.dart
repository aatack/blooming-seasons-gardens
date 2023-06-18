import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:flutter/material.dart';

import '../../models/structs/point.dart';

class PointInput extends StatelessWidget {
  final Point point;
  final void Function(Point, bool) onChange;

  const PointInput({super.key, required this.point, required this.onChange});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        const Text("Horizontal"),
        const SizedBox(width: 5),
        Container(
          color: Colors.white,
          child: ControlledTextInput(
            value: point.x.string,
            onChange: (newValue, transient) {
              onChange(Point(point.x.set(newValue), point.y), transient);
            },
          ),
        ),
        const SizedBox(width: 20),
        const Text("Vertical"),
        const SizedBox(width: 5),
        Container(
          color: Colors.white,
          child: ControlledTextInput(
            value: point.y.string,
            onChange: (newValue, transient) {
              onChange(Point(point.x, point.y.set(newValue)), transient);
            },
          ),
        ),
      ],
    );
  }
}
