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
          offset: const Offset(-50, -50),
          child: GestureDetector(
            onTap: () {},
            child: Container(
              width: 100,
              height: 100,
              decoration: const BoxDecoration(
                  shape: BoxShape.circle, color: Colors.red),
            ),
          ),
        )
      ],
    );
  }
}
