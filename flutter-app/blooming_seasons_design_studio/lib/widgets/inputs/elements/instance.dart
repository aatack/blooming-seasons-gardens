import 'package:flutter/material.dart' hide Element;

import '../../../models/garden/arrow.dart';
import '../../../models/garden/instance.dart';
import '../../../models/garden/label.dart';
import '../../../models/garden/plant.dart';

class InstanceEditor extends StatelessWidget {
  final Instance<Element> instance;

  const InstanceEditor({super.key, required this.instance});

  @override
  Widget build(BuildContext context) {
    late final Widget content;

    if (instance.element is Plant) {
      content = Text("Plant");
    } else if (instance.element is Label) {
      content = Text("Label");
    } else if (instance.element is Arrow) {
      return Text("Arrow");
    } else {
      throw UnimplementedError();
    }

    return content;
  }
}
