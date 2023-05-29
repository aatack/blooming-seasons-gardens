import 'package:flutter/material.dart';

import '../../models/garden/garden.dart';

class EditGarden extends StatelessWidget {
  final Garden garden;

  const EditGarden({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    return Text(garden.name);
  }
}
