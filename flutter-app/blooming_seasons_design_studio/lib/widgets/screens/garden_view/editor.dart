import 'package:flutter/material.dart';

import '../../wrappers/resizable.dart';

class Editor extends StatelessWidget {
  const Editor({super.key});

  @override
  Widget build(BuildContext context) {
    // return ResizableArea();
    return FractionallySizedBox(
      // widthFactor: 0.25,
      // heightFactor: 1.0,
      // child: ListView(
      //   children: const [
      //     Collapsible(child: Placeholder()),
      //     Collapsible(child: Placeholder()),
      //     Collapsible(child: Placeholder()),
      //     Collapsible(child: Placeholder()),
      //   ],
      // ),
      child: Resizable(initialWidth: 200, child: Placeholder()),
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
          child: Placeholder(),
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
