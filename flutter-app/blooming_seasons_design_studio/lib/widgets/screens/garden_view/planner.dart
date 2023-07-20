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
  Offset _position = const Offset(0, 0);
  double _scale = 1;

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (context, constraints) {
      return TopDown(
        width: constraints.maxWidth,
        height: constraints.maxHeight,
        position: _position,
        scale: _scale,
        setPosition: (newPosition) {
          setState(() {
            _position = newPosition;
          });
        },
        setScale: (newScale) {
          setState(() {
            _scale = newScale;
          });
        },
        onHoveredElementChanged: (id) {
          context
              .read<SessionState>()
              .updateSelections((selections) => selections.withHovered(id));
        },
        onSelectedElementChanged: (id) {
          context.read<SessionState>().updateSelections((selections) =>
              // Deselect the element if it is already selected
              selections.withSelected(selections.selected == id ? null : id));
        },
        child: widget.painter,
      );
    });
  }
}
