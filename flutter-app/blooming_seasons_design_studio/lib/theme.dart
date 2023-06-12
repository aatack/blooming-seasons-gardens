import 'dart:ui';

import 'package:flutter/material.dart' hide Color;

class AppTheme {
  static MaterialColor backgroundColour =
      _createMaterialColour(const Color.fromARGB(255, 201, 248, 228));
  static MaterialColor neutralColour =
      _createMaterialColour(const Color.fromARGB(255, 139, 206, 185));
  static MaterialColor foregroundColour =
      _createMaterialColour(const Color.fromARGB(255, 78, 166, 153));

  static MaterialColor emphasiseColour =
      _createMaterialColour(const Color.fromARGB(255, 20, 13, 79));

  static MaterialColor darkColour =
      _createMaterialColour(const Color.fromARGB(255, 28, 11, 25));
  static MaterialColor lightColour =
      _createMaterialColour(const Color.fromARGB(255, 247, 247, 242));
}

MaterialColor _createMaterialColour(Color colour) {
  List strengths = <double>[.05];

  final swatch = <int, Color>{};
  final int red = colour.red, green = colour.green, blue = colour.blue;

  for (int i = 1; i < 10; i++) {
    strengths.add(0.1 * i);
  }
  strengths.forEach((strength) {
    final double delta = 0.5 - strength;

    swatch[(strength * 1000).round()] = Color.fromRGBO(
      red + ((delta < 0 ? red : (255 - red)) * delta).round(),
      green + ((delta < 0 ? green : (255 - green)) * delta).round(),
      blue + ((delta < 0 ? blue : (255 - blue)) * delta).round(),
      1,
    );
  });

  return MaterialColor(colour.value, swatch);
}
