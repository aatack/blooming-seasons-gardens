import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:flutter/material.dart';

import '../../models/garden/bed.dart';
import '../wrappers/collapsible.dart';

class BedView extends StatelessWidget {
  final Bed bed;

  const BedView({super.key, required this.bed});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: Collapsible(
        header: Text(bed.name),
        child: Row(children: [
          ControlledTextInput(value: bed.name, onChange: (newValue) {})
        ]),
      ),
    );
  }
}
