import 'package:flutter/material.dart';

class Hoverable extends StatefulWidget {
  final Widget Function(BuildContext context, bool hovered, bool clicked)
      builder;
  final void Function() onTap;

  const Hoverable({super.key, required this.builder, required this.onTap});

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
        cursor: SystemMouseCursors.click,
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
  final void Function() onTap;

  const HoverableIcon({
    super.key,
    required this.icon,
    required this.height,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Hoverable(
      builder: (context, hovered, clicked) => Icon(
        icon,
        color: (hovered && !clicked) ? Colors.grey[700] : Colors.white,
        size: height,
      ),
      onTap: onTap,
    );
  }
}
