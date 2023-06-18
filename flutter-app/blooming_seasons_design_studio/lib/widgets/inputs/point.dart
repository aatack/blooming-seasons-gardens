import 'package:blooming_seasons_design_studio/models/inputs/validated.dart';
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
        _wrapTextInput(
          point.x,
          (newValue, transient) {
            onChange(Point(point.x.set(newValue), point.y), transient);
          },
        ),
        const SizedBox(width: 20),
        const Text("Vertical"),
        const SizedBox(width: 5),
        _wrapTextInput(
          point.y,
          (newValue, transient) {
            onChange(Point(point.x, point.y.set(newValue)), transient);
          },
        ),
      ],
    );
  }

  Widget _wrapTextInput(
      ValidatedDouble value, void Function(String, bool) onInputChange) {
    return Tooltip(
      message: value.errors.isEmpty ? "" : value.errors.join("\n"),
      excludeFromSemantics: true, // Prevents tooltip from grabbing focus
      child: Container(
        color: value.errors.isEmpty ? Colors.white : Colors.red[100],
        child: Padding(
          padding: const EdgeInsets.only(left: 5, right: 3),
          child: ControlledTextInput(
            value: value.string,
            onChange: onInputChange,
          ),
        ),
      ),
    );
  }
}
