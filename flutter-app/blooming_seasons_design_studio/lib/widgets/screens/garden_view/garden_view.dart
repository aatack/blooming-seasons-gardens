import 'package:flutter/material.dart';

import '../../../models/garden/garden.dart';
import 'editor/editor.dart';
import 'planner.dart';

class GardenView extends StatelessWidget {
  final Garden garden;

  const GardenView({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      mainAxisSize: MainAxisSize.max,
      children: [
        Expanded(
          child: Stack(
            children: [
              Planner(garden: garden),
              Editor(garden: garden),
            ],
          ),
        ),
      ],
    );
  }
}
