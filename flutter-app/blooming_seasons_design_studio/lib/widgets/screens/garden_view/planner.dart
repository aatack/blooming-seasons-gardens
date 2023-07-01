import 'package:blooming_seasons_design_studio/widgets/top_down.dart';
import 'package:flutter/material.dart';

class Planner extends StatefulWidget {
  const Planner({
    super.key,
  });

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
      children: [
        Transform.translate(
          offset: const Offset(50, 50),
          transformHitTests: true,
          child: GestureDetector(
            // TODO: work out how to capture gestures when the offset is negative
            onTap: () {
              print("Clicked circle");
            },
            child: Container(
              width: 100,
              height: 100,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.red,
                border: Border.all(color: Colors.black, width: 2),
              ),
            ),
          ),
        ),
        GestureDetector(
          onTap: () {
            print("Clicked");
          },
          child: CustomPaint(
            painter: LinePainter(
              startPoint: Offset(50, 50), // Starting position of the line
              endPoint: Offset(200, 200), // Ending position of the line
              color: Colors.black, // Color of the line
              strokeWidth: 2.0, // Width of the line
            ),
          ),
        )
      ],
    );
  }
}

class LinePainter extends CustomPainter {
  final Offset startPoint;
  final Offset endPoint;
  final Color color;
  final double strokeWidth;

  LinePainter({
    required this.startPoint,
    required this.endPoint,
    required this.color,
    required this.strokeWidth,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = strokeWidth
      ..style = PaintingStyle.stroke;

    final path = Path()
      ..moveTo(startPoint.dx, startPoint.dy)
      ..lineTo(endPoint.dx, endPoint.dy);

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}
