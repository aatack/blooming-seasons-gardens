import 'package:flutter/material.dart';

import '../../../models/garden/label.dart';

class LabelEditor extends StatelessWidget {
  final Label label;

  const LabelEditor({super.key, required this.label});

  @override
  Widget build(BuildContext context) {
    return Text("Label");
  }
}
