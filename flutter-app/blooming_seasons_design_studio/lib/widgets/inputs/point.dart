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
    return Table(
      defaultColumnWidth: const IntrinsicColumnWidth(),
      children: [
        TableRow(
          children: [
            const TableCell(
                child: Padding(
              padding: EdgeInsets.only(right: 10, bottom: 8),
              child: Text("Horizontal"),
            )),
            TableCell(
                child: _wrapTextInput(
              point.x,
              (newValue, transient) {
                onChange(Point(point.x.set(newValue), point.y), transient);
              },
            )),
          ],
        ),
        TableRow(
          children: [
            const TableCell(child: Text("Vertical")),
            TableCell(
                child: _wrapTextInput(
              point.y,
              (newValue, transient) {
                onChange(Point(point.x, point.y.set(newValue)), transient);
              },
            )),
          ],
        ),
      ],
    );
  }

  Widget _wrapTextInput(
      ValidatedDouble value, void Function(String, bool) onInputChange) {
    final content = Container(
      color: value.errors.isEmpty ? Colors.white : Colors.red[100],
      child: Padding(
        padding: const EdgeInsets.only(left: 5, right: 3),
        child: ControlledTextInput(
          value: value.string,
          onChange: onInputChange,
        ),
      ),
    );

    return Row(
      children: [
        content,
        Visibility(
          visible: value.errors.isNotEmpty,
          maintainSize: true,
          maintainAnimation: true,
          maintainState: true,
          /* For some reason, simply using a tooltip here causes the
            tooltip to grab focus every time the message goes from empty
            to non-empty.  This solution doesn't grab focus, and hence
            doesn't interfere with the text input. */
          child: Padding(
            padding: const EdgeInsets.only(left: 5),
            child: Tooltip(
              message: value.errors.join("\n"),
              child: const Icon(Icons.error_outline),
            ),
          ),
        )
      ],
    );
  }
}
