import 'package:flutter/material.dart';

import 'instance.dart';

@immutable
class Arrow implements BedElement {
  final double x;
  final double y;

  const Arrow(this.x, this.y);
}
