import 'package:flutter/material.dart';

import '../../models/garden/bed.dart';

class BedWidget extends StatelessWidget {
  final Bed bed;

  const BedWidget({super.key, required this.bed});

  @override
  Widget build(BuildContext context) {
    return const SizedBox(height: 200, child: Placeholder());
  }
}
