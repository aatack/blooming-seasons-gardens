import 'package:flutter/material.dart';

import 'instance.dart';

@immutable
class Label implements BedElement {
  final String text;
  final double size;

  const Label(this.text, this.size);
}
