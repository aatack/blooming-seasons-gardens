import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

@immutable
class TopDownPosition {
  final double x;
  final double y;
  final double scale;

  const TopDownPosition(this.x, this.y, this.scale);

  Offset worldPosition(Offset screenPosition) {
    return Offset(
        (screenPosition.dx - x) / scale, (screenPosition.dy - y) / scale);
  }

  double worldDistance(double screenDistance) {
    return screenDistance / scale;
  }
}

class TopDown extends StatefulWidget {
  final TopDownPosition position;
  final void Function(TopDownPosition) setPosition;
  final void Function(int?)? onHoveredElementChanged;
  final void Function(int?)? onSelectedElementChanged;

  final Painter child;

  const TopDown(
      {super.key,
      required this.position,
      required this.setPosition,
      this.onHoveredElementChanged,
      this.onSelectedElementChanged,
      required this.child});

  @override
  State<TopDown> createState() => _TopDownState();
}

class _TopDownState extends State<TopDown> {
  Offset? _dragOrigin;
  TopDownPosition? _positionOrigin;
  int? _hoveredElement;

  @override
  Widget build(BuildContext context) {
    return FractionallySizedBox(
      widthFactor: 1,
      heightFactor: 1,
      child: _wrapInControls(_transformedChildren()),
    );
  }

  Widget _wrapInControls(Widget child) {
    return Listener(
      onPointerSignal: (PointerSignalEvent signal) {
        if (signal is PointerScrollEvent) {
          _doScroll(signal.scrollDelta.dy, signal.localPosition);
        }
      },
      onPointerHover: (event) {
        final hovered = widget.child
            .hitTest(widget.position.worldPosition(event.localPosition));
        if (hovered != _hoveredElement &&
            widget.onHoveredElementChanged != null) {
          setState(() {
            _hoveredElement = hovered;
          });
          widget.onHoveredElementChanged!(hovered);
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
        onPanEnd: (_) {
          setState(() {
            _dragOrigin = null;
            _positionOrigin = null;
          });
        },
        onTapUp: (TapUpDetails details) {
          if (widget.onSelectedElementChanged != null) {
            widget.onSelectedElementChanged!(widget.child
                .hitTest(widget.position.worldPosition(details.localPosition)));
          }
        },
        child: MouseRegion(
            cursor: _hoveredElement == null
                ? (_dragOrigin == null
                    ? SystemMouseCursors.grab
                    : SystemMouseCursors.grabbing)
                : SystemMouseCursors.click,
            child: child),
      ),
    );
  }

  void _doScroll(double scrollAmount, Offset screenPosition) {
    if (_dragOrigin == null) {
      // A typical scroll amount is 100 units per scroll, so we zoom in or out
      // by 10% per roll of the scroll wheel
      final double factor = (1 + (0.001 * scrollAmount.abs()));
      final double ratio = scrollAmount < 0 ? 1 * factor : 1 / factor;

      final x =
          screenPosition.dx - ratio * (screenPosition.dx - widget.position.x);
      final y =
          screenPosition.dy - ratio * (screenPosition.dy - widget.position.y);

      widget.setPosition(
        TopDownPosition(x, y, widget.position.scale * ratio),
      );
    }
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
          alignment: Alignment.topLeft,
          scale: widget.position.scale,
          transformHitTests: true,
          child: CustomPaint(painter: _TopDownPainter(widget.child)),
        ),
      ),
    );
  }
}

class _TopDownPainter extends CustomPainter {
  final Painter child;

  const _TopDownPainter(this.child);

  @override
  void paint(Canvas canvas, Size size) {
    child.paint(canvas);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

abstract class Painter {
  void paint(Canvas canvas);

  int? hitTest(Offset position);
}

class PainterGroup extends Painter {
  final Offset offset;
  final List<Painter> children;
  final void Function(Canvas)? paintBackground;

  PainterGroup(this.offset, this.children, {this.paintBackground});

  @override
  int? hitTest(Offset position) {
    // When checking for hits, iterate backwards through children such
    // that the child that is rendered last gets hit first
    for (final child in children.reversed) {
      final hitResult = child.hitTest(position - offset);
      if (hitResult != null) {
        return hitResult;
      }
    }
    return null;
  }

  @override
  void paint(Canvas canvas) {
    canvas.save();
    canvas.translate(offset.dx, offset.dy);

    if (paintBackground != null) {
      paintBackground!(canvas);
    }

    for (final child in children) {
      child.paint(canvas);
    }

    canvas.restore();
  }
}
