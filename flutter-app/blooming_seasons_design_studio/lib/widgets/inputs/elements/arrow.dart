import 'package:blooming_seasons_design_studio/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:flutter/material.dart' hide Element;

import '../../../models/garden/arrow.dart';
import '../../../models/garden/instance.dart';
import '../../../models/structs/point.dart';
import '../../top_down.dart';
import '../point.dart';

class ArrowEditor extends StatelessWidget {
  final Arrow arrow;
  final void Function(Element, bool) setElement;

  final Point position;
  final void Function(Point, bool) setPosition;

  final bool hidePosition;

  const ArrowEditor({
    super.key,
    required this.arrow,
    required this.setElement,
    required this.position,
    required this.setPosition,
    this.hidePosition = false,
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
        if (!hidePosition)
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

class ArrowPainter extends Painter {
  final Offset start = Offset(50, 50);
  final Offset end = Offset(200, 200);
  final Color colour = Colors.black;
  final double thickness = 2;

  @override
  void paint(Canvas canvas) {
    final paint = Paint()
      ..color = colour
      ..strokeWidth = thickness
      ..style = PaintingStyle.stroke;

    final path = Path()
      ..moveTo(start.dx, start.dy)
      ..lineTo(end.dx, end.dy);

    canvas.drawPath(path, paint);
  }

  @override
  int? hitTest(Offset position) {
    return null;
  }
}
