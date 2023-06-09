import 'package:flutter/material.dart';

@immutable
abstract class UserEntered<Type> {
  final String string;

  const UserEntered(this.string);

  bool get valid;
  Type get value;
}

class UserEnteredDouble extends UserEntered<double> {
  final double? minimum;
  final double? maximum;

  const UserEnteredDouble(super.string, {this.minimum, this.maximum});

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

  UserEnteredDouble deserialise(Map<String, dynamic> userEnteredDouble) {
    return UserEnteredDouble(
      userEnteredDouble["string"],
      minimum: userEnteredDouble["minimum"],
      maximum: userEnteredDouble["maximum"],
    );
  }
}
