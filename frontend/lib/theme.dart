import 'package:flutter/material.dart';

const lightColorScheme = ColorScheme(
  brightness: Brightness.light,
  primary: Color(0xFF006B5C),
  onPrimary: Color(0xFFFFFFFF),
  primaryContainer: Color(0xFF77F8DF),
  onPrimaryContainer: Color(0xFF00201B),
  secondary: Color(0xFF006B5F),
  onSecondary: Color(0xFFFFFFFF),
  secondaryContainer: Color(0xFF75F8E3),
  onSecondaryContainer: Color(0xFF00201C),
  tertiary: Color(0xFF705D00),
  onTertiary: Color(0xFFFFFFFF),
  tertiaryContainer: Color(0xFFFFE174),
  onTertiaryContainer: Color(0xFF221B00),
  error: Color(0xFFBA1A1A),
  errorContainer: Color(0xFFFFDAD6),
  onError: Color(0xFFFFFFFF),
  onErrorContainer: Color(0xFF410002),
  background: Color(0xFFFFFBFF),
  onBackground: Color(0xFF2E004E),
  surface: Color(0xFFFFFBFF),
  onSurface: Color(0xFF2E004E),
  surfaceVariant: Color(0xFFDAE5E1),
  onSurfaceVariant: Color(0xFF3F4946),
  outline: Color(0xFF6F7976),
  onInverseSurface: Color(0xFFFBECFF),
  inverseSurface: Color(0xFF461968),
  inversePrimary: Color(0xFF58DBC3),
  shadow: Color(0xFF000000),
  surfaceTint: Color(0xFF006B5C),
  outlineVariant: Color(0xFFBEC9C5),
  scrim: Color(0xFF000000),
);

const darkColorScheme = ColorScheme(
  brightness: Brightness.dark,
  primary: Color(0xFF58DBC3),
  onPrimary: Color(0xFF00382F),
  primaryContainer: Color(0xFF005045),
  onPrimaryContainer: Color(0xFF77F8DF),
  secondary: Color(0xFF54DBC8),
  onSecondary: Color(0xFF003731),
  secondaryContainer: Color(0xFF005047),
  onSecondaryContainer: Color(0xFF75F8E3),
  tertiary: Color(0xFFE4C44A),
  onTertiary: Color(0xFF3B2F00),
  tertiaryContainer: Color(0xFF554500),
  onTertiaryContainer: Color(0xFFFFE174),
  error: Color(0xFFFFB4AB),
  errorContainer: Color(0xFF93000A),
  onError: Color(0xFF690005),
  onErrorContainer: Color(0xFFFFDAD6),
  background: Color(0xFF2E004E),
  onBackground: Color(0xFFF2DAFF),
  surface: Color(0xFF2E004E),
  onSurface: Color(0xFFF2DAFF),
  surfaceVariant: Color(0xFF3F4946),
  onSurfaceVariant: Color(0xFFBEC9C5),
  outline: Color(0xFF89938F),
  onInverseSurface: Color(0xFF2E004E),
  inverseSurface: Color(0xFFF2DAFF),
  inversePrimary: Color(0xFF006B5C),
  shadow: Color(0xFF000000),
  surfaceTint: Color(0xFF58DBC3),
  outlineVariant: Color(0xFF3F4946),
  scrim: Color(0xFF000000),
);

Color lighter(Color colour, {int amount = 10}) {
  return Color.fromARGB(colour.alpha, colour.red + amount,
      colour.green + amount, colour.blue + amount);
}

Color darker(Color colour, {int amount = 10}) {
  return lighter(colour, amount: -amount);
}
