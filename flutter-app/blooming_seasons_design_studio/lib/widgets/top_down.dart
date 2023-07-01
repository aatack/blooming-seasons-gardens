import 'package:flutter/material.dart';

@immutable
class TopDownPosition {
  final double x;
  final double y;
  final double scale;

  const TopDownPosition(this.x, this.y, this.scale);
}

class TopDown extends StatefulWidget {
  final TopDownPosition position;
  final void Function(TopDownPosition) setPosition;

  final List<Widget> children;

  const TopDown(
      {super.key,
      required this.position,
      required this.setPosition,
      required this.children});

  @override
  State<TopDown> createState() => _TopDownState();
}

class _TopDownState extends State<TopDown> {
  Offset? _dragOrigin;
  TopDownPosition? _positionOrigin;

  @override
  Widget build(BuildContext context) {
    return FractionallySizedBox(
      widthFactor: 1,
      heightFactor: 1,
      child: Stack(
        children: [
          GestureDetector(
            onPanStart: (details) {
              setState(() {
                _dragOrigin = details.globalPosition;
                _positionOrigin = widget.position;
              });
            },
            onPanUpdate: (details) {
              widget.setPosition(TopDownPosition(
                _positionOrigin!.x -
                    (_dragOrigin!.dx - details.globalPosition.dx),
                _positionOrigin!.y -
                    (_dragOrigin!.dy - details.globalPosition.dy),
                widget.position.scale,
              ));
            },
            child: Container(color: Colors.white),
          ),
          Positioned(
              left: widget.position.x,
              top: widget.position.y,
              child: SizedBox(
                width: double.maxFinite,
                height: double.maxFinite,
                child: Stack(children: widget.children),
              )),
        ],
      ),
    );
  }
}
