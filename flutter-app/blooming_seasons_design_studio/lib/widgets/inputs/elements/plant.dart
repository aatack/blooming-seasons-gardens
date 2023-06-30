import 'package:flutter/material.dart' hide Element;

import '../../../models/garden/instance.dart';
import '../../../models/garden/plant.dart';
import '../../../models/structs/point.dart';

class PlantEditor extends StatelessWidget {
  final Plant plant;
  final void Function(Element, bool) setElement;

  final Point position;
  final void Function(Point, bool) setPosition;

  const PlantEditor({
    super.key,
    required this.plant,
    required this.setElement,
    required this.position,
    required this.setPosition,
  });

  @override
  Widget build(BuildContext context) {
    return Text("Plant");
  }
}
