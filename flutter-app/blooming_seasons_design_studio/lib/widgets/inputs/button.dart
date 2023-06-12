import 'package:flutter/material.dart';

class Button extends StatelessWidget {
  final void Function()? onClicked;
  final Widget child;
  final bool emphasise;

  const Button({
    super.key,
    required this.onClicked,
    required this.child,
    this.emphasise = false,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(onPressed: onClicked, child: child);
  }
}
