import 'package:flutter/material.dart';

import '../../../models/garden/arrow.dart';

class ArrowEditor extends StatelessWidget {
  final Arrow arrow;

  const ArrowEditor({super.key, required this.arrow});

  @override
  Widget build(BuildContext context) {
    return Text("Arrow");
  }
}
