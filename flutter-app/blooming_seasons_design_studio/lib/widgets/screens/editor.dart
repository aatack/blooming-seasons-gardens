import 'package:flutter/material.dart';

import '../../models/garden.dart';

class GardenEditor extends StatelessWidget {
  final Garden garden;

  const GardenEditor({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    return Text(garden.name);
  }
}
