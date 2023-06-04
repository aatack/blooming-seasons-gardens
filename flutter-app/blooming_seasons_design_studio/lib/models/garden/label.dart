import 'package:flutter/material.dart' show immutable;

import 'package:image/image.dart' show Image;
import 'instance.dart';

@immutable
class Label implements Element {
  final String text;
  final double size;

  const Label({required this.text, required this.size});

  @override
  dynamic serialise(
    Map<int, dynamic> templates,
    Map<Image, int> images,
  ) {
    return {
      "elementType": "label",
      "text": text,
      "size": size,
    };
  }
}

Label deserialiseLabel(dynamic label) {
  return Label(text: label["text"], size: label["size"]);
}
