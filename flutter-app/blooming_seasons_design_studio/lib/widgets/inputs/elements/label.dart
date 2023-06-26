import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../models/garden/label.dart';
import '../../../models/inputs/validated.dart';
import '../../../models/session.dart';
import '../../../models/structs/point.dart';
import '../form_layout.dart';
import '../point.dart';
import '../text.dart';

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
    return FormLayout(
      children: [
        FormLayoutItem(
          label: const Text("Text"),
          child: validatedTextInput(
            label.text,
            (newText, transient) {
              context.read<SessionState>().editGarden((garden) => garden);
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
