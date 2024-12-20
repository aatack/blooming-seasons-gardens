import 'dart:math';

import 'package:blooming_seasons_gardens/constants.dart';
import 'package:blooming_seasons_gardens/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_gardens/widgets/inputs/text.dart';
import 'package:flutter/material.dart' hide Element;

import '../../../models/garden/arrow.dart';
import '../../../models/garden/instance.dart';
import '../../../models/selections.dart';
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
  final Arrow arrow;

  // Whether the instance or its parent bed is hovered or selected
  final bool hovered;
  final bool selected;

  late final Offset _source;
  late final Paint _paint;
  late final Path _path;

  ArrowPainter(this.arrow, {required this.hovered, required this.selected}) {
    _source = arrow.source.offset;

    _paint = Paint()
      ..color = hovered
          ? hoveredColour
          : selected
              ? selectedColour
              : Colors.black
      ..strokeWidth = arrow.thickness.output * (hovered || selected ? 1.5 : 1)
      ..style = PaintingStyle.stroke;

    _path = Path()
      ..moveTo(0, 0)
      ..lineTo(_source.dx, _source.dy);
  }

  @override
  void paint(Canvas canvas) {
    canvas.drawPath(_path, _paint);
  }

  @override
  bool contains(Offset position) {
    final along =
        ((position.dx - 0) * _source.dx + (position.dy - 0) * _source.dy) /
            _source.distance;
    final normal =
        ((position.dx - 0) * -_source.dy + (position.dy - 0) * _source.dx) /
            _source.distance;

    final leeway = arrow.thickness.output * 2;

    return (-leeway <= along) &&
        (along <= _source.distance + leeway) &&
        (normal.abs() <= leeway);
  }
}
