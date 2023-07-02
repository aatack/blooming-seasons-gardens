import 'package:blooming_seasons_design_studio/widgets/inputs/elements/bed.dart';
import 'package:blooming_seasons_design_studio/widgets/top_down.dart';
import 'package:flutter/material.dart';

import '../../../models/garden/garden.dart';

class Planner extends StatefulWidget {
  final Garden garden;

  const Planner({super.key, required this.garden});

  @override
  State<Planner> createState() => _PlannerState();
}

class _PlannerState extends State<Planner> {
  TopDownPosition _position = const TopDownPosition(0, 0, 1);

  @override
  Widget build(BuildContext context) {
    return TopDown(
      position: _position,
      setPosition: (newPosition) {
        setState(() {
          _position = newPosition;
        });
      },
      child: PainterGroup(Offset(0, 0),
          widget.garden.beds.map((bed) => BedPainter(bed)).toList()),
    );
  }
}

class PlantPainter extends Painter {
  @override
  void paint(Canvas canvas) {
    canvas.save();
    canvas.translate(-100, -100);
    canvas.scale(2);

    canvas.drawCircle(Offset.zero, 20, Paint()..color = Colors.blue);

    canvas.restore();
  }

  @override
  int? hitTest(Offset position) {
    return null;
  }
}

class ArrowPainter extends Painter {
  final Offset start = Offset(50, 50);
  final Offset end = Offset(200, 200);
  final Color colour = Colors.black;
  final double thickness = 2;

  @override
  void paint(Canvas canvas) {
    final paint = Paint()
      ..color = colour
      ..strokeWidth = thickness
      ..style = PaintingStyle.stroke;

    final path = Path()
      ..moveTo(start.dx, start.dy)
      ..lineTo(end.dx, end.dy);

    canvas.drawPath(path, paint);
  }

  @override
  int? hitTest(Offset position) {
    return null;
  }
}
