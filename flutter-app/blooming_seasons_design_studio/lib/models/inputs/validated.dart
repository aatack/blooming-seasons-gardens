import 'package:flutter/material.dart';

@immutable
class ValidationResult<DataType> {
  final List<String> errors;
  final DataType? result;

  const ValidationResult(this.errors, this.result);

  bool get isValid => errors.isEmpty;
}

@immutable
abstract class Validated<DataType,
    OwnType extends Validated<DataType, OwnType>> {
  final String input;
  final DataType output;

  const Validated(this.input, this.output);

  ValidationResult<DataType> validate(String candidate);

  OwnType update(String newInput);

  List<String> get errors => validate(input).errors;
  bool get isValid => errors.isEmpty;
}

class UnvalidatedString extends Validated<String, UnvalidatedString> {
  const UnvalidatedString(super.input, super.output);

  factory UnvalidatedString.initialise(String input) {
    return UnvalidatedString(input, input);
  }

  @override
  ValidationResult<String> validate(String candidate) {
    return ValidationResult(const [], candidate);
  }

  @override
  UnvalidatedString update(String newInput) {
    return UnvalidatedString(newInput, newInput);
  }
}

class ValidatedDouble extends Validated<double, ValidatedDouble> {
  final double? minimum;
  final double? maximum;

  const ValidatedDouble(super.input, super.output,
      {this.minimum, this.maximum});

  factory ValidatedDouble.initialise(double output,
      {double? minimum, double? maximum}) {
    return ValidatedDouble(output.toString(), output,
        minimum: minimum, maximum: maximum);
  }

  @override
  ValidationResult<double> validate(String candidate) {
    final parsedValue = double.tryParse(candidate);
    return ValidationResult(
      [
        if (parsedValue == null) "Value is not a valid number",
        if ((minimum != null) &&
            (parsedValue != null) &&
            (parsedValue < minimum!))
          "Value must be greater than or equal to $minimum",
        if ((maximum != null) &&
            (parsedValue != null) &&
            (parsedValue > maximum!))
          "Value must be less than or equal to $maximum",
      ],
      parsedValue,
    );
  }

  @override
  ValidatedDouble update(String newInput) {
    final result = validate(newInput);
    return ValidatedDouble(
      newInput,
      result.isValid ? result.result! : output,
      minimum: minimum,
      maximum: maximum,
    );
  }

  Map<String, dynamic> serialise() {
    return {
      "input": input,
      "output": output,
      if (minimum != null) "minimum": minimum,
      if (maximum != null) "maximum": maximum,
    };
  }

  static ValidatedDouble deserialise(Map<String, dynamic> validated) {
    return ValidatedDouble(
      validated["input"],
      validated["output"],
      minimum: validated.containsKey("minimum") ? validated["minimum"] : null,
      maximum: validated.containsKey("maximum") ? validated["maximum"] : null,
    );
  }
}
