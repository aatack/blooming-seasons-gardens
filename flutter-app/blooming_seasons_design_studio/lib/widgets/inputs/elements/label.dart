import 'package:blooming_seasons_design_studio/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/point.dart';
import 'package:flutter/material.dart';

import '../../../models/garden/label.dart';
import '../../../models/structs/point.dart';

class LabelEditor extends StatelessWidget {
  final Label label;
  final Point position;
  final void Function(Point, bool) setPosition;

  const LabelEditor({
    super.key,
    required this.label,
    required this.position,
    required this.setPosition,
  });

  @override
  Widget build(BuildContext context) {
    return FormLayout(children: [
      FormLayoutItem(
          label: const Text("Position"),
          child: PointInput(
            point: position,
            onChange: setPosition,
          )),
    ]);
  }
}
