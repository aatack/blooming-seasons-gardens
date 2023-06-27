import 'package:flutter/material.dart' hide Element;

import '../../../models/garden/instance.dart';
import '../../../models/garden/label.dart';
import '../../../models/structs/point.dart';
import '../form_layout.dart';
import '../point.dart';
import '../text.dart';

class LabelEditor extends StatelessWidget {
  final Label label;
  final void Function(Element, bool) setElement;

  final Point position;
  final void Function(Point, bool) setPosition;

  const LabelEditor({
    super.key,
    required this.label,
    required this.setElement,
    required this.position,
    required this.setPosition,
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
        ...pointInput(
          label: "Position",
          point: position,
          setPoint: setPosition,
        ),
      ],
    );
  }
}
