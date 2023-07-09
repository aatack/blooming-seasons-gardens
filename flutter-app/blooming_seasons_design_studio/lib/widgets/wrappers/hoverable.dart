import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class Hoverable extends StatefulWidget {
  final Widget Function(BuildContext context, bool hovered, bool clicked)
      builder;
  final void Function() onTap;
  final SystemMouseCursor? cursor;

  const Hoverable(
      {super.key, required this.builder, required this.onTap, this.cursor});

  @override
  State<Hoverable> createState() => _HoverableState();
}

class _HoverableState extends State<Hoverable> {
  bool _hovered = false;
  bool _clicked = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) {
        setState(() {
          _clicked = true;
        });
      },
      onTapUp: (_) {
        setState(() {
          _clicked = false;
        });
      },
      onTap: () {
        widget.onTap();
      },
      child: MouseRegion(
        cursor:
            widget.cursor == null ? SystemMouseCursors.click : widget.cursor!,
        onEnter: (_) {
          setState(() {
            _hovered = true;
          });
        },
        onExit: (_) {
          setState(() {
            _hovered = false;
            _clicked = false;
          });
        },
        child: widget.builder(context, _hovered, _clicked),
      ),
    );
  }
}

class HoverableIcon extends StatelessWidget {
  final IconData icon;
  final double height;
  final void Function()? onTap;
  final Color? colour;
  final Color? hoverColour;
  final Color? clickColour;

  const HoverableIcon(
      {super.key,
      required this.icon,
      required this.height,
      required this.onTap,
      required this.colour,
      required this.hoverColour,
      required this.clickColour});

  @override
  Widget build(BuildContext context) {
    return Hoverable(
      builder: (context, hovered, clicked) => Icon(
        icon,
        color: (clicked || onTap == null)
            ? clickColour
            : hovered
                ? hoverColour
                : colour,
        size: height,
      ),
      onTap: onTap == null ? () {} : onTap!,
      cursor: onTap == null ? SystemMouseCursors.forbidden : null,
    );
  }
}
