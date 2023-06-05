import 'package:flutter/material.dart';

class Resizable extends StatefulWidget {
  final double initialWidth;
  final Widget child;

  const Resizable({super.key, required this.initialWidth, required this.child});

  @override
  State<Resizable> createState() => _ResizableState();
}

class _ResizableState extends State<Resizable> {
  late double _width;

  final double _padding = 20;

  @override
  void initState() {
    super.initState();
    _width = widget.initialWidth;
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        SizedBox(
          width: _width,
          child: widget.child,
        ),
        MouseRegion(
          cursor: SystemMouseCursors.grab,
          child: GestureDetector(
            onHorizontalDragUpdate: (details) {
              // I'm not sure how, but this condition somehow also prevents the
              // area from being made too big
              if (details.globalPosition.dx > 0) {
                setState(
                  () {
                    _width += details.delta.dx;
                    if (_width < _padding) {
                      _width = _padding;
                    }
                  },
                );
              }
            },
            child: Container(
              width: 6,
              color: Colors.grey[300],
            ),
          ),
        )
      ],
    );
    ;
  }
}
