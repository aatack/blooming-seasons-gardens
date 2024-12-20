import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class TopDown extends StatefulWidget {
  final double width;
  final double height;
  final Offset position;
  final double scale;

  final void Function(Offset, double) setPositionAndScale;

  final bool Function(BuildContext, Offset)? handleClick;
  final bool Function(BuildContext, Offset)? handleMove;

  final Painter child;

  const TopDown(
      {super.key,
      required this.width,
      required this.height,
      required this.position,
      required this.scale,
      required this.setPositionAndScale,
      this.handleClick,
      this.handleMove,
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
  void Function(BuildContext, Offset?)? _dragHandler;

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
        final position = widget.worldPosition(event.localPosition);
        final handled = widget.child.handleMove(context, position);

        if (!handled && widget.handleMove != null) {
          widget.handleMove!(context, position);
        }
      },
      child: GestureDetector(
        onPanStart: (details) {
          final dragHandler = widget.child
              .handleDrag(context, widget.worldPosition(details.localPosition));
          final worldOrigin = widget.position;

          setState(() {
            _dragOriginScreen = details.localPosition;
            _dragHandler = dragHandler ??
                (_, worldOffset) {
                  if (worldOffset != null) {
                    widget.setPositionAndScale(
                        worldOrigin + worldOffset, widget.scale);
                  }
                };
          });
        },
        onPanUpdate: (details) {
          if (_dragHandler != null) {
            // Assumes that the scale has not changed during dragging
            final worldOffset = Offset(
                widget.worldDistance(
                    _dragOriginScreen!.dx - details.localPosition.dx),
                widget.worldDistance(
                    _dragOriginScreen!.dy - details.localPosition.dy));

            _dragHandler!(context, worldOffset);
          }
        },
        onPanEnd: (details) {
          if (_dragHandler != null) {
            _dragHandler!(context, null);
          }

          setState(() {
            _dragOriginScreen = null;
            _dragHandler = null;
          });
        },
        onTapUp: (TapUpDetails details) {
          final position = widget.worldPosition(details.localPosition);
          final handled = widget.child.handleClick(context, position);

          if (!handled && (widget.handleClick != null)) {
            widget.handleClick!(context, position);
          }
        },
        child: MouseRegion(
            cursor: widget.child.cursor() ??
                (_dragOriginScreen == null
                    ? SystemMouseCursors.grab
                    : SystemMouseCursors.grabbing),
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

      /* Derive by setting the world position of the mouse after the change
        to be equal to its position before the change. */
      final x = widget.position.dx +
          (((1 / widget.scale) - (1 / (ratio * widget.scale))) *
              (screenPosition.dx - (widget.width / 2)));
      final y = widget.position.dy +
          (((1 / widget.scale) - (1 / (ratio * widget.scale))) *
              (screenPosition.dy - (widget.height / 2)));

      widget.setPositionAndScale(Offset(x, y), widget.scale * ratio);
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
        child: Transform.scale(
          alignment: Alignment.topLeft,
          scale: widget.scale,
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

  bool contains(Offset position) {
    return false;
  }

  bool handleClick(BuildContext context, Offset position) {
    return false;
  }

  bool handleMove(BuildContext context, Offset position) {
    return false;
  }

  void Function(BuildContext, Offset?)? handleDrag(
      BuildContext context, Offset position) {
    // Should optionally return a function taking the new build context,
    // a drag offset (ie. the current mouse position relative to its position
    // at the start of the drag) in the world coordinates.  If the function
    // is being called for the final time, the coordinates will be `null`
    return null;
  }

  SystemMouseCursor? cursor() {
    return null;
  }
}

class PainterGroup extends Painter {
  final Offset offset;
  final List<Painter> children;
  final void Function(Canvas)? paintBackground;

  PainterGroup(this.offset, this.children, {this.paintBackground});

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

  @override
  bool contains(Offset position) {
    // When checking for hits, iterate backwards through children such
    // that the child that is rendered last gets hit first
    for (final child in children.reversed) {
      if (child.contains(position - offset)) {
        return true;
      }
    }
    return false;
  }

  @override
  bool handleClick(BuildContext context, Offset position) {
    for (final child in children.reversed) {
      if (child.handleClick(context, position - offset)) {
        return true;
      }
    }
    return false;
  }

  @override
  bool handleMove(BuildContext context, Offset position) {
    for (final child in children.reversed) {
      if (child.handleMove(context, position - offset)) {
        return true;
      }
    }
    return false;
  }

  @override
  void Function(BuildContext, Offset?)? handleDrag(
      BuildContext context, Offset position) {
    for (final child in children.reversed) {
      final childHandler = child.handleDrag(context, position - offset);
      if (childHandler != null) {
        return childHandler;
      }
    }
    return null;
  }

  @override
  SystemMouseCursor? cursor() {
    for (final child in children.reversed) {
      final cursor = child.cursor();
      if (cursor != null) {
        return cursor;
      }
    }
    return null;
  }
}
