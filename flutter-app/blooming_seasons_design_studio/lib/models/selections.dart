import 'package:flutter/material.dart';

@immutable
class Selections {
  final int? selectedGarden;
  final int? hoveredGarden;

  final int? selectedNursery;
  final int? hoveredNursery;

  const Selections(
      {this.selectedGarden,
      this.hoveredGarden,
      this.selectedNursery,
      this.hoveredNursery});
}
