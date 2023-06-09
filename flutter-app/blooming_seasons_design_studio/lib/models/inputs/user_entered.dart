import 'package:flutter/material.dart';

@immutable
abstract class UserEntered<Type> {
  final String string;

  const UserEntered(this.string);

  bool get valid;
  Type get value;
}
