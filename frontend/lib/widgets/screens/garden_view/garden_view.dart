import 'package:blooming_seasons_gardens/models/selections.dart';
import 'package:flutter/material.dart';

import '../../../models/garden/garden.dart';
import 'editor/editor.dart';
import 'planner.dart';

class GardenView extends StatelessWidget {
  final Garden garden;
  final Selections selections;

  const GardenView({super.key, required this.garden, required this.selections});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      mainAxisSize: MainAxisSize.max,
      children: [
        Expanded(
          child: Stack(
            children: [
              Planner(garden: garden, selections: selections),
              Editor(garden: garden, selections: selections),
            ],
          ),
        ),
      ],
    );
  }
}
