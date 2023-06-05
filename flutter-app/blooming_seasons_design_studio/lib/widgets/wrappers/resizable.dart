import 'package:flutter/material.dart';

class Resizable extends StatelessWidget {
  final double initialWidth;
  final Widget child;

  const Resizable({super.key, required this.initialWidth, required this.child});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        SizedBox(
          width: initialWidth,
          child: child,
        ),
        MouseRegion(
          cursor: SystemMouseCursors.grab,
          child: GestureDetector(
            onHorizontalDragUpdate: (details) {},
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
