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
        child: Column(
          children: garden.beds.map((bed) => BedWidget(bed: bed)).toList(),
        ),
      ),
    );
  }
}

class ResizableArea extends StatefulWidget {
  @override
  _ResizableAreaState createState() => _ResizableAreaState();
}

class _ResizableAreaState extends State<ResizableArea> {
  double _width = 200.0; // Initial width of the resizable area
  final double _minWidth = 20.0;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      cursor: SystemMouseCursors.grab,
      child: GestureDetector(
        onHorizontalDragUpdate: (details) {
          // I'm not sure how, but this condition somehow also prevents the
          // area from being made too big
          if (details.globalPosition.dx > 0) {
            setState(
              () {
                _width += details.delta.dx;
                if (_width < _minWidth) {
                  _width = _minWidth;
                }
              },
            );
          }
        },
        child: Container(
          width: _width,
          height: 200.0, // Height of the resizable area
          color: Colors.blue,
          child: const Placeholder(),
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
