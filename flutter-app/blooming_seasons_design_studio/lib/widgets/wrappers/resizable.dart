import 'package:flutter/material.dart';

class Resizable extends StatelessWidget {
  final int initialWidth;
  final Widget child;

  const Resizable({super.key, required this.initialWidth, required this.child});

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      cursor: SystemMouseCursors.grab,
      child: GestureDetector(
        onHorizontalDragUpdate: (details) {},
        child: Container(
          width: 200.0,
          child: child,
        ),
      ),
    );
  }
}
