import 'package:blooming_seasons_design_studio/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
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
    return Column(
      children: [
        FormLayout(
          children: [
            FormLayoutItem(
              label: const Text("Diameter"),
              child: validatedTextInput(
                plant.diameter,
                (newDiameter, transient) {
                  setElement(plant.resize(newDiameter), transient);
                },
              ),
            ),
          ],
        ),
      ],
    );
  }
}
