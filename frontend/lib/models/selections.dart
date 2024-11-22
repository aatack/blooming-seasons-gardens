import 'package:flutter/material.dart';

enum EditorTab { garden, nursery, background }

@immutable
class Selections {
  final EditorTab editorTab;

  final int? selected;
  final int? hovered;

  const Selections({required this.editorTab, this.selected, this.hovered});

  static Selections blank() {
    return const Selections(editorTab: EditorTab.garden);
  }

  Selections withEditorTab(EditorTab newTab) {
    return Selections(editorTab: newTab, hovered: hovered, selected: selected);
  }

  Selections withSelected(int? newSelected) {
    return Selections(
        editorTab: editorTab, selected: newSelected, hovered: hovered);
  }

  Selections withHovered(int? newHovered) {
    return Selections(
        editorTab: editorTab, selected: selected, hovered: newHovered);
  }
}
