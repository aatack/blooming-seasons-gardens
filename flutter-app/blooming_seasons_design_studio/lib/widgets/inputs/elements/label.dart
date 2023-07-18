import 'package:blooming_seasons_design_studio/constants.dart';
import 'package:blooming_seasons_design_studio/widgets/top_down.dart';
import 'package:flutter/material.dart' hide Element;

import '../../../models/garden/instance.dart';
import '../../../models/garden/label.dart';
import '../../../models/selections.dart';
import '../../../models/structs/point.dart';
import '../form_layout.dart';
import '../point.dart';
import '../text.dart';

class LabelEditor extends StatelessWidget {
  final Label label;
  final void Function(Element, bool) setElement;

  final Point position;
  final void Function(Point, bool) setPosition;

  final bool hidePosition;

  const LabelEditor({
    super.key,
    required this.label,
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
          label: const Text("Text"),
          child: validatedTextInput(
            label.text,
            (newText, transient) {
              setElement(Label(text: newText, size: label.size), transient);
            },
          ),
        ),
        FormLayoutItem(
          label: const Text("Size"),
          child: validatedTextInput(
            label.size,
            (newSize, transient) {
              setElement(Label(text: label.text, size: newSize), transient);
            },
          ),
        ),
        if (!hidePosition)
          ...pointInput(
            label: "Position",
            point: position,
            setPoint: setPosition,
          ),
      ],
    );
  }
}

class LabelPainter extends Painter {
  final Label label;
  final int id;

  // Whether the instance or its parent bed is hovered or selected
  final bool hovered;
  final bool selected;

  late final TextSpan _text;
  late final TextPainter _painter;

  LabelPainter(this.label, this.id, {required this.hovered, required this.selected}) {
    _text = TextSpan(
      text: label.text.output,
      style: TextStyle(
        color: hovered
            ? hoveredColour
            : selected
                ? selectedColour
                : Colors.black,
        fontSize: label.size.output,
        fontWeight: FontWeight.bold,
        fontFamily: "Spectral",
        fontFamilyFallback: const ["Arial"],
      ),
    );

    _painter = TextPainter(text: _text, textDirection: TextDirection.ltr);
    _painter.layout();
  }

  @override
  int? hitTest(Offset position) {
    return null;
  }

  @override
  void paint(Canvas canvas) {
    _painter.paint(canvas, const Offset(0, 0));
  }
}
