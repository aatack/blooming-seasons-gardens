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
          _wrapInControls(_transformedChildren()),
          // Text(
          //     "x=${widget.position.x} y=${widget.position.y} scale=${widget.position.scale}"),
          if (_dragOrigin != null)
            Text(
                "x=${_worldPosition(_dragOrigin!).dx} y=${_worldPosition(_dragOrigin!).dy}"),
        ],
      ),
    );
  }

  Offset _worldPosition(Offset screenPosition) {
    return Offset(
      screenPosition.dx - widget.position.x,
      screenPosition.dy - widget.position.y,
    );
  }

  Widget _wrapInControls(Widget child) {
    return Listener(
      onPointerSignal: (PointerSignalEvent signal) {
        if (signal is PointerScrollEvent) {
          _doScroll(signal.scrollDelta.dy);
        }
      },
      child: GestureDetector(
        onPanStart: (details) {
          setState(() {
            _dragOrigin = details.localPosition;
            _positionOrigin = widget.position;
          });
        },
        onPanUpdate: (details) {
          widget.setPosition(TopDownPosition(
            _positionOrigin!.x - (_dragOrigin!.dx - details.localPosition.dx),
            _positionOrigin!.y - (_dragOrigin!.dy - details.localPosition.dy),
            widget.position.scale,
          ));
        },
        child: child,
      ),
    );
  }

  void _doScroll(double scrollAmount) {
    // A typical scroll amount is 100 units per scroll, so we zoom in or out
    // by 10% per roll of the scroll wheel
    final double factor = (1 + (0.001 * scrollAmount.abs()));

    widget.setPosition(
      TopDownPosition(
        widget.position.x,
        widget.position.y,
        scrollAmount < 0
            ? widget.position.scale * factor
            : widget.position.scale / factor,
      ),
    );
  }

  Widget _transformedChildren() {
    return Container(
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
    );
  }
}
