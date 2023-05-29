import 'package:flutter/material.dart' show immutable;

import 'package:image/image.dart' show Image;
import 'instance.dart';

@immutable
class Label implements BedElement {
  final String text;
  final double size;

  const Label(this.text, this.size);

  @override
  dynamic serialise(
    Map<int, dynamic> templates,
    Map<Image, int> images,
  ) {
    return {
      "text": text,
      "size": size,
    };
  }
}
