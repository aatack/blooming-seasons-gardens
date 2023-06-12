import 'package:flutter/material.dart';

import '../../theme.dart';
import 'hoverable.dart';

class ClickableCard extends StatelessWidget {
  final Widget child;
  final Color? colour;
  final void Function()? onClick;
  final Widget? overlay;

  static const double _height = 20;

  const ClickableCard(
      {super.key,
      required this.child,
      this.colour,
      this.onClick,
      this.overlay});

  @override
  Widget build(BuildContext context) {
    final colour = this.colour ?? Theme.of(context).colorScheme.surfaceVariant;

    return Hoverable(
      builder: (context, hovered, clicked) => Card(
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.zero),
        color: clicked
            ? darker(darker(colour))
            : (hovered ? darker(colour) : colour),
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: SizedBox(
            height: _height,
            child: Stack(
              children: [
                Align(
                  alignment: Alignment.centerLeft,
                  child: child,
                ),
                if (overlay != null) _overlayed(context, overlay!),
              ],
            ),
          ),
        ),
      ),
      onTap: onClick ?? () {},
    );
  }

  Widget _overlayed(BuildContext context, Widget widget) {
    return Align(
      alignment: Alignment.centerRight,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [widget],
      ),
    );
  }
}
