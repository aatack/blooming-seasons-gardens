import 'package:blooming_seasons_design_studio/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:flutter/material.dart' hide Element;

import '../../../models/garden/arrow.dart';
import '../../../models/garden/instance.dart';
import '../../../models/structs/point.dart';
import '../point.dart';

class ArrowEditor extends StatelessWidget {
  final Arrow arrow;
  final void Function(Element, bool) setElement;

  final Point position;
  final void Function(Point, bool) setPosition;

  const ArrowEditor({
    super.key,
    required this.arrow,
    required this.setElement,
    required this.position,
    required this.setPosition,
  });

  @override
  Widget build(BuildContext context) {
    return FormLayout(
      children: [
        FormLayoutItem(
            label: const Text("Thickness"),
            child:
                validatedTextInput(arrow.thickness, (newThickness, transient) {
              setElement(arrow.withThickness(newThickness), transient);
            })),
        ...pointInput(
          label: "Start",
          point: arrow.source,
          setPoint: (newSource, transient) => setElement(
            arrow.withSource(newSource),
            transient,
          ),
        ),
        ...pointInput(
          label: "End",
          point: position,
          setPoint: setPosition,
        ),
      ],
    );
  }
}
