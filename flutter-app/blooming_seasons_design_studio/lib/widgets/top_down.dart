import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

class TopDown extends StatefulWidget {
  final double width;
  final double height;
  final Offset position;
  final double scale;

  final void Function(Offset) setPosition;
  final void Function(double) setScale;

  final void Function(int?)? onHoveredElementChanged;
  final void Function(int?)? onSelectedElementChanged;

  final Painter child;

  const TopDown(
      {super.key,
      required this.width,
      required this.height,
      required this.position,
      required this.scale,
      required this.setPosition,
      required this.setScale,
      this.onHoveredElementChanged,
      this.onSelectedElementChanged,
      required this.child});

  @override
  State<TopDown> createState() => _TopDownState();

  Offset worldPosition(Offset screenPosition) => Offset(
        position.dx + worldDistance(screenPosition.dx - (width / 2)),
        position.dy + worldDistance(screenPosition.dy - (height / 2)),
      );

  double worldDistance(double screenDistance) => screenDistance / scale;
}

class _TopDownState extends State<TopDown> {
  Offset? _dragOriginScreen;
  Offset? _dragOriginWorld;
  int? _hoveredElement;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.width,
      height: widget.height,
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
        final hovered =
            widget.child.hitTest(widget.worldPosition(event.localPosition));
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
            _dragOriginScreen = details.localPosition;
            _dragOriginWorld = widget.position;
          });
        },
        onPanUpdate: (details) {
          // Assumes that the scale has not changed during dragging
          final worldOffset = Offset(
              widget.worldDistance(
                  _dragOriginScreen!.dx - details.localPosition.dx),
              widget.worldDistance(
                  _dragOriginScreen!.dy - details.localPosition.dy));

          widget.setPosition(_dragOriginWorld! + worldOffset);
        },
        onPanEnd: (_) {
          setState(() {
            _dragOriginScreen = null;
            _dragOriginWorld = null;
          });
        },
        onTapUp: (TapUpDetails details) {
          if (widget.onSelectedElementChanged != null) {
            widget.onSelectedElementChanged!(widget.child
                .hitTest(widget.worldPosition(details.localPosition)));
          }
        },
        child: MouseRegion(
            cursor: _hoveredElement == null
                ? (_dragOriginScreen == null
                    ? SystemMouseCursors.grab
                    : SystemMouseCursors.grabbing)
                : SystemMouseCursors.click,
            child: child),
      ),
    );
  }

  void _doScroll(double scrollAmount, Offset screenPosition) {
    if (_dragOriginScreen == null) {
      // A typical scroll amount is 100 units per scroll, so we zoom in or out
      // by 10% per roll of the scroll wheel
      final double factor = (1 + (0.001 * scrollAmount.abs()));
      final double ratio = scrollAmount < 0 ? 1 * factor : 1 / factor;

      final x =
          screenPosition.dx - ratio * (screenPosition.dx - widget.position.dx);
      final y =
          screenPosition.dy - ratio * (screenPosition.dy - widget.position.dy);

      widget.setScale(widget.scale * ratio);
      // widget.setPosition(Offset(x, y));
    }
  }

  Widget _transformedChildren() {
    return Container(
      width: double.maxFinite,
      height: double.maxFinite,
      color: Colors.white,
      child: Transform.translate(
        offset: Offset(
          (widget.position.dx * -widget.scale) + (widget.width / 2),
          (widget.position.dy * -widget.scale) + (widget.height / 2),
        ),
        transformHitTests: true,
        child: Transform.scale(
          alignment: Alignment.topLeft,
          scale: widget.scale,
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
