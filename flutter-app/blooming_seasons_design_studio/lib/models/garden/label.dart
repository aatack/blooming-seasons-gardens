import 'package:blooming_seasons_design_studio/models/inputs/validated.dart';
import 'package:flutter/material.dart' show immutable;

import 'package:image/image.dart' show Image;
import 'instance.dart';

@immutable
class Label implements Element {
  final UnvalidatedString text;
  final ValidatedDouble size;

  const Label({required this.text, required this.size});

  @override
  dynamic serialise(
    Map<int, dynamic> templates,
    Map<Image, int> images,
  ) {
    return {
      "elementType": "label",
      "text": text.string,
      "size": size.serialise(),
    };
  }
}

Label deserialiseLabel(dynamic label) {
  return Label(
      text: UnvalidatedString(label["text"]),
      size: ValidatedDouble.deserialise(label["size"]));
}
