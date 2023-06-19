import 'package:flutter/material.dart' hide Element;

import '../../../models/garden/arrow.dart';
import '../../../models/garden/instance.dart';
import '../../../models/garden/label.dart';
import '../../../models/garden/plant.dart';
import '../../../theme.dart';
import '../../wrappers/hoverable.dart';
import '../point.dart';

class InstanceEditor extends StatefulWidget {
  final Instance<Element> instance;

  const InstanceEditor({super.key, required this.instance});

  @override
  State<InstanceEditor> createState() => _InstanceEditorState();
}

class _InstanceEditorState extends State<InstanceEditor> {
  bool _collapsed = true;

  @override
  Widget build(BuildContext context) {
    late final Widget content;

    if (widget.instance.element is Plant) {
      content = const Text("Plant");
    } else if (widget.instance.element is Label) {
      content = const Text("Label");
    } else if (widget.instance.element is Arrow) {
      return const Text("Arrow");
    } else {
      throw UnimplementedError();
    }

    final colour = Colors.grey[100]!;
    final hoverColour = darker(colour, amount: 10);
    final clickColour = darker(colour, amount: 20);

    return Hoverable(
      onTap: () {
        setState(() {
          _collapsed = !_collapsed;
        });
      },
      builder: (context, hovered, clicked) {
        return Container(
          color: clicked
              ? clickColour
              : hovered
                  ? hoverColour
                  : colour,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Divider(),
              content,
              if (!_collapsed)
                PointInput(
                    point: widget.instance.position,
                    onChange: (newPosition, transient) {}),
            ],
          ),
        );
      },
    );
  }
}
