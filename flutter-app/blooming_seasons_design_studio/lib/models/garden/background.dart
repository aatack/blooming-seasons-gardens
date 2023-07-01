import 'package:blooming_seasons_design_studio/models/inputs/validated.dart';
import 'package:blooming_seasons_design_studio/models/structs/point.dart';
import 'package:flutter/material.dart';

@immutable
class Background {
  final String? image;
  final Point position;
  final ValidatedDouble scale;

  const Background({required this.image, required this.position, required this.scale});
}