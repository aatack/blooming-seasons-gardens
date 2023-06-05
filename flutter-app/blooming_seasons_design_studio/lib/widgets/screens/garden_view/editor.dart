import 'package:flutter/material.dart';

import '../../../models/garden/garden.dart';
import '../../elements/bed.dart';
import '../../wrappers/resizable.dart';

class Editor extends StatelessWidget {
  final Garden garden;

  const Editor({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    return FractionallySizedBox(
      child: Resizable(
        initialWidth: 200,
        child: Container(
          color: Colors.white,
          child: Column(
            children: garden.beds.map((bed) => BedWidget(bed: bed)).toList(),
          ),
        ),
      ),
    );
  }
}
