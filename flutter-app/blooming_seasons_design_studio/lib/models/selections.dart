import 'package:flutter/material.dart';

enum EditorTab { garden, nursery, background }

@immutable
class Selections {
  final EditorTab editorTab;

  final int? selectedGarden;
  final int? hoveredGarden;

  final int? selectedNursery;
  final int? hoveredNursery;

  const Selections(
      {required this.editorTab,
      this.selectedGarden,
      this.hoveredGarden,
      this.selectedNursery,
      this.hoveredNursery});

  static Selections blank() {
    return const Selections(editorTab: EditorTab.garden);
  }

  Selections withEditorTab(EditorTab newTab) {
    return Selections(
        editorTab: newTab,
        selectedGarden: selectedGarden,
        hoveredGarden: hoveredGarden,
        selectedNursery: selectedNursery,
        hoveredNursery: hoveredNursery);
  }
}
