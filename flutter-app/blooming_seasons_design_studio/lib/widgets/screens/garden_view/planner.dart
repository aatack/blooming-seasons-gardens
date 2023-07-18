import 'package:blooming_seasons_design_studio/models/selections.dart';
import 'package:blooming_seasons_design_studio/models/session.dart';
import 'package:blooming_seasons_design_studio/models/structs/positioned_image.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/elements/bed.dart';
import 'package:blooming_seasons_design_studio/widgets/top_down.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../models/garden/garden.dart';

class Planner extends StatefulWidget {
  final Garden garden;
  final Selections selections;

  late final PainterGroup painter;

  Planner({super.key, required this.garden, required this.selections}) {
    painter = PainterGroup(
      const Offset(0, 0),
      [
        PositionedImagePainter(garden.background),
        ...garden.beds
            .map((bed) => BedPainter(bed, garden.nursery, selections))
            .toList()
      ],
    );
  }

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
      onHoveredElementChanged: (id) {
        context
            .read<SessionState>()
            .updateSelections((selections) => selections.withHovered(id));
      },
      onSelectedElementChanged: (id) {
        context
            .read<SessionState>()
            .updateSelections((selections) => selections.withSelected(id));
      },
      child: widget.painter,
    );
  }
}
