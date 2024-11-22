import 'package:flutter/material.dart';

class Button extends StatelessWidget {
  final void Function()? onClicked;
  final Widget child;
  final bool emphasise;
  final Color? backgroundColour;

  const Button({
    super.key,
    required this.onClicked,
    required this.child,
    this.emphasise = false,
    this.backgroundColour,
  });

  @override
  Widget build(BuildContext context) {
    return OutlinedButton(
      onPressed: onClicked,
      style: TextButton.styleFrom(
          shape: const RoundedRectangleBorder(
            borderRadius: BorderRadius.zero,
          ),
          backgroundColor: backgroundColour),
      child: child,
    );
  }
}
