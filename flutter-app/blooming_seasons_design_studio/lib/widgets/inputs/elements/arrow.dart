import 'package:flutter/material.dart';

import '../../../models/garden/arrow.dart';
import '../../../models/structs/point.dart';

class ArrowEditor extends StatelessWidget {
  final Arrow arrow;
  final Point position;
  final void Function(Point, bool) setPosition;

  const ArrowEditor({
    super.key,
    required this.arrow,
    required this.position,
    required this.setPosition,
  });

  @override
  Widget build(BuildContext context) {
    return Text("Arrow");
  }
}
