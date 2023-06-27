import 'package:flutter/material.dart';

@immutable
abstract class Validated<DataType,
    OwnType extends Validated<DataType, OwnType>> {
  final String string;

  const Validated(this.string);

  List<String> get errors;
  DataType get value;

  Validated<DataType, OwnType> set(String newString);
}

class UnvalidatedString extends Validated<String, UnvalidatedString> {
  const UnvalidatedString(super.string);

  @override
  List<String> get errors => [];

  @override
  String get value => string;

  @override
  UnvalidatedString set(String newString) {
    return UnvalidatedString(newString);
  }
}

class ValidatedDouble extends Validated<double, ValidatedDouble> {
  final double? minimum;
  final double? maximum;

  const ValidatedDouble(super.string, {this.minimum, this.maximum});

  @override
  List<String> get errors => _errors();

  List<String> _errors() {
    final parsedValue = double.tryParse(string);
    return [
      if (parsedValue == null) "Value is not a valid number",
      if ((minimum != null) &&
          (parsedValue != null) &&
          (parsedValue < minimum!))
        "Value must be greater than or equal to $minimum",
      if ((maximum != null) &&
          (parsedValue != null) &&
          (parsedValue > maximum!))
        "Value must be less than or equal to $maximum",
    ];
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

  static ValidatedDouble deserialise(Map<String, dynamic> validated) {
    return ValidatedDouble(
      validated["string"],
      minimum: validated["minimum"],
      maximum: validated["maximum"],
    );
  }

  @override
  ValidatedDouble set(String newString) {
    return ValidatedDouble(newString, minimum: minimum, maximum: maximum);
  }
}
