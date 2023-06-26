import 'package:flutter/material.dart';

import '../../../models/garden/label.dart';
import '../../../models/structs/point.dart';

class LabelEditor extends StatelessWidget {
  final Label label;
  final Point position;
  final void Function(Point) setPosition;

  const LabelEditor({
    super.key,
    required this.label,
    required this.position,
    required this.setPosition,
  });

  @override
  Widget build(BuildContext context) {
    return Text("Label");
  }
}
