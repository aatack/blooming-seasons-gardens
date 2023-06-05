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

  final double _padding = 50;
  final double _handleWidth = 6;

  @override
  void initState() {
    super.initState();
    _width = widget.initialWidth;
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (context, constraints) {
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
                if (details.globalPosition.dx > 0 &&
                    details.globalPosition.dx < constraints.maxWidth) {
                  setState(
                    () {
                      _width += details.delta.dx;
                      if (_width < _padding) {
                        _width = _padding;
                      }
                      if (_width >
                          constraints.maxWidth - _handleWidth - _padding) {
                        _width = constraints.maxWidth - _handleWidth - _padding;
                      }
                    },
                  );
                }
              },
              child: Container(
                width: _handleWidth,
                color: Colors.grey[300],
              ),
            ),
          )
        ],
      );
    });
    ;
  }
}
