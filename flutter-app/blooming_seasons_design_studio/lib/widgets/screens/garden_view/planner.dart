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
