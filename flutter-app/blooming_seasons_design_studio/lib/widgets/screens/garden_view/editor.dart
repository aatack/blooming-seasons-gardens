import 'package:flutter/material.dart';

import '../../../models/garden/garden.dart';
import '../../elements/bed.dart';
import '../../wrappers/resizable.dart';

class Editor extends StatelessWidget {
  final Garden garden;

  const Editor({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    return FractionallySizedBox(
      child: Resizable(
        initialWidth: 200,
        child: Container(
          color: Colors.white,
          child: Column(
            children: garden.beds.map((bed) => BedWidget(bed: bed)).toList(),
          ),
        ),
      ),
    );
  }
}

class Collapsible extends StatefulWidget {
  const Collapsible({super.key, required this.child});

  final Widget child;

  @override
  State<Collapsible> createState() => _CollapsibleState();
}

class _CollapsibleState extends State<Collapsible> {
  bool _collapsed = false;

  @override
  Widget build(BuildContext context) {
    List<Widget> children = [
      ElevatedButton(
        onPressed: () {
          setState(() {
            _collapsed = !_collapsed;
          });
        },
        child: const Text("Expand"),
      )
    ];

    if (!_collapsed) {
      children.add(widget.child);
    }

    return Column(mainAxisSize: MainAxisSize.min, children: children);
  }
}
