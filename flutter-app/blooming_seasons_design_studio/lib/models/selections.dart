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

  Selections withSelectedGarden(int? newSelectedGarden) {
    return Selections(
        editorTab: editorTab,
        selectedGarden: newSelectedGarden,
        hoveredGarden: hoveredGarden,
        selectedNursery: selectedNursery,
        hoveredNursery: hoveredNursery);
  }

  Selections withHoveredGarden(int? newHoveredGarden) {
    return Selections(
        editorTab: editorTab,
        selectedGarden: selectedGarden,
        hoveredGarden: newHoveredGarden,
        selectedNursery: selectedNursery,
        hoveredNursery: hoveredNursery);
  }

  Selections withSelectedNursery(int? newSelectedNursery) {
    return Selections(
        editorTab: editorTab,
        selectedGarden: selectedGarden,
        hoveredGarden: hoveredGarden,
        selectedNursery: newSelectedNursery,
        hoveredNursery: hoveredNursery);
  }

  Selections withHoveredNursery(int? newHoveredNursery) {
    return Selections(
        editorTab: editorTab,
        selectedGarden: selectedGarden,
        hoveredGarden: hoveredGarden,
        selectedNursery: selectedNursery,
        hoveredNursery: newHoveredNursery);
  }
}
