import 'package:blooming_seasons_gardens/models/session.dart';
import 'package:blooming_seasons_gardens/widgets/inputs/button.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../../models/garden/garden.dart';
import '../../../../models/selections.dart';
import '../../../inputs/elements/bed.dart';

class GardenTab extends StatelessWidget {
  final Garden garden;
  final Selections selections;

  const GardenTab({super.key, required this.garden, required this.selections});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: FractionallySizedBox(
        heightFactor: 1.0,
        child: Padding(
          padding: const EdgeInsets.only(left: 8.0, right: 8.0, top: 4.0),
          child: ListView(
            children: [
              ...garden.beds
                  .map((bed) => Column(
                        children: [
                          BedEditor(
                              bed: bed,
                              nursery: garden.nursery,
                              selections: selections),
                          const SizedBox(height: 8.0)
                        ],
                      ))
                  .toList(),
              Button(
                onClicked: () {
                  context
                      .read<SessionState>()
                      .editGarden((garden) => garden.addBed());
                },
                child: const Text("Add bed"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
