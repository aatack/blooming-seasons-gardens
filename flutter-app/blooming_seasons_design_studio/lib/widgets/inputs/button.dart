import 'package:flutter/material.dart';

import '../../theme.dart';

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
    final colour =
        emphasise ? AppTheme.emphasiseColour : AppTheme.foregroundColour;

    return TextButton(
      onPressed: onClicked,
      style: TextButton.styleFrom(
          backgroundColor: colour,
          shape: const RoundedRectangleBorder(borderRadius: BorderRadius.zero)),
      child: child,
    );
  }
}
