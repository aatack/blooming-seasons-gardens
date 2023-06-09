import 'package:flutter/material.dart';

@immutable
abstract class Validated<Type> {
  final String string;

  const Validated(this.string);

  bool get valid;
  Type get value;
}

class ValidatedDouble extends Validated<double> {
  final double? minimum;
  final double? maximum;

  const ValidatedDouble(super.string, {this.minimum, this.maximum});

  @override
  bool get valid => _valid();

  bool _valid() {
    final parsedValue = double.tryParse(string);
    return parsedValue != null &&
        (minimum == null || parsedValue >= minimum!) &&
        (maximum == null || parsedValue <= maximum!);
  }

  @override
  double get value => double.parse(string);

  Map<String, dynamic> serialise() {
    return {
      "string": string,
      "minimum": minimum,
      "maximum": maximum,
    };
  }

  ValidatedDouble deserialise(Map<String, dynamic> validated) {
    return ValidatedDouble(
      validated["string"],
      minimum: validated["minimum"],
      maximum: validated["maximum"],
    );
  }
}
