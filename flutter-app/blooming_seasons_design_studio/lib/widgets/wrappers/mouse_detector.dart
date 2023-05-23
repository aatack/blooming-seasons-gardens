import 'package:flutter/material.dart';

class MouseDetector extends StatelessWidget {
  final Widget Function(BuildContext bool, bool) builder;

  const MouseDetector({super.key, required this.builder});

  @override
  Widget build(BuildContext context) {
    return const Placeholder();
  }
}
