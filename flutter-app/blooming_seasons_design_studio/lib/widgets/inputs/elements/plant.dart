import 'package:flutter/material.dart';

import '../../../models/garden/plant.dart';

class PlantEditor extends StatelessWidget {
  final Plant plant;

  const PlantEditor({super.key, required this.plant});

  @override
  Widget build(BuildContext context) {
    return Text("Plant");
  }
}
