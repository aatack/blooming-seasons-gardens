import 'package:blooming_seasons_gardens/models/inputs/validated.dart';
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
      "text": text.input,
      "size": size.serialise(),
    };
  }

  static Label blank() {
    return Label(
      text: UnvalidatedString.initialise("Label"),
      size: ValidatedDouble.initialise(20),
    );
  }
}

Label deserialiseLabel(dynamic label) {
  return Label(
      text: UnvalidatedString.initialise(label["text"]),
      size: ValidatedDouble.deserialise(label["size"]));
}
