import 'package:flutter/gestures.dart';
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
          Listener(
            onPointerSignal: (PointerSignalEvent signal) {
              if (signal is PointerScrollEvent) {
                widget.setPosition(
                  TopDownPosition(
                    widget.position.x,
                    widget.position.y,
                    signal.scrollDelta.dy < 0
                        ? widget.position.scale * 1.1
                        : widget.position.scale / 1.1,
                  ),
                );
              }
            },
            child: GestureDetector(
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
              child: Container(
                width: double.maxFinite,
                height: double.maxFinite,
                color: Colors.white,
                child: Transform.translate(
                  offset: Offset(widget.position.x, widget.position.y),
                  transformHitTests: true,
                  child: Transform.scale(
                    scale: widget.position.scale,
                    child: Stack(children: widget.children),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
