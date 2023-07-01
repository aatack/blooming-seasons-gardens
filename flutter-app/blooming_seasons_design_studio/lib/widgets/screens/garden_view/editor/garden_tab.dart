
import 'package:flutter/material.dart';

import '../../../../models/garden/bed.dart';
import '../../../inputs/elements/bed.dart';

class GardenTab extends StatelessWidget {
  final List<Bed> beds;

  const GardenTab({super.key, required this.beds});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: FractionallySizedBox(
        heightFactor: 1.0,
        child: Padding(
          padding: const EdgeInsets.only(left: 8.0, right: 8.0, top: 4.0),
          child: ListView(
            children: beds
                .map((bed) => Column(
                      children: [
                        BedEditor(bed: bed),
                        const SizedBox(height: 8.0)
                      ],
                    ))
                .toList(),
          ),
        ),
      ),
    );
  }
}