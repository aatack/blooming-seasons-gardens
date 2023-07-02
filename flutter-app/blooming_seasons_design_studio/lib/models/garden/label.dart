import 'package:blooming_seasons_design_studio/models/inputs/validated.dart';
import 'package:flutter/material.dart' show immutable;

import 'instance.dart';

@immutable
class Label implements Element {
  final UnvalidatedString text;
  final ValidatedDouble size;

  const Label({required this.text, required this.size});

  @override
  dynamic serialise() {
    return {
      "elementType": "label",
      "text": text.string,
      "size": size.serialise(),
    };
  }

  static Label blank() {
    return const Label(
      text: UnvalidatedString("Label"),
      size: ValidatedDouble("20"),
    );
  }
}

Label deserialiseLabel(dynamic label) {
  return Label(
      text: UnvalidatedString(label["text"]),
      size: ValidatedDouble.deserialise(label["size"]));
}
