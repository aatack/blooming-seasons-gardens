import 'dart:convert';

import 'package:blooming_seasons_design_studio/models/session.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../../models/garden/garden.dart';
import '../../../../models/modals.dart';
import '../../../../models/selections.dart';
import '../../../inputs/button.dart';
import '../../../wrappers/resizable.dart';
import 'background_tab.dart';
import 'garden_tab.dart';
import 'nursery_tab.dart';

const bool _debug = false;

class Editor extends StatefulWidget {
  final Garden garden;
  final Selections selections;

  const Editor({super.key, required this.garden, required this.selections});

  @override
  State<Editor> createState() => _EditorState();
}

class _EditorState extends State<Editor> {
  @override
  Widget build(BuildContext context) {
    return FractionallySizedBox(
      heightFactor: 1.0,
      child: Resizable(
        initialWidth: 400,
        child: Container(
          color: Colors.white,
          child: Column(
            children: [
              _TabButtons(
                garden: widget.garden,
                tab: widget.selections.editorTab,
                setTab: (newTab) {
                  context.read<SessionState>().updateSelections(
                      (selections) => selections.withEditorTab(newTab));
                },
              ),
              if (widget.selections.editorTab == EditorTab.garden)
                GardenTab(garden: widget.garden, selections: widget.selections),
              if (widget.selections.editorTab == EditorTab.nursery)
                NurseryTab(nursery: widget.garden.nursery),
              if (widget.selections.editorTab == EditorTab.background)
                BackgroundTab(background: widget.garden.background),
            ],
          ),
        ),
      ),
    );
  }
}

class _TabButtons extends StatelessWidget {
  final Garden garden;
  final EditorTab tab;
  final void Function(EditorTab) setTab;

  const _TabButtons(
      {required this.garden, required this.tab, required this.setTab});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Button(
          onClicked: () {
            setTab(EditorTab.garden);
          },
          backgroundColour: tab == EditorTab.garden
              ? Theme.of(context).colorScheme.surfaceVariant
              : null,
          child: const Text(
            "Garden",
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
        Button(
          onClicked: () {
            setTab(EditorTab.nursery);
          },
          backgroundColour: tab == EditorTab.nursery
              ? Theme.of(context).colorScheme.surfaceVariant
              : null,
          child: const Text(
            "Nursery",
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
        Button(
          onClicked: () {
            setTab(EditorTab.background);
          },
          backgroundColour: tab == EditorTab.background
              ? Theme.of(context).colorScheme.surfaceVariant
              : null,
          child: const Text(
            "Background",
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
        if (_debug)
          Button(
            onClicked: () {
              const encoder = JsonEncoder.withIndent("  ");

              final serialisation = serialiseGarden(garden);
              serialisation["images"] = serialisation["images"].map(
                  (id, image) =>
                      MapEntry(id, "<image with ${image.length} bytes>"));

              final text = Text(
                encoder.convert(serialisation),
                style: const TextStyle(fontFamily: "Monospace"),
              );

              context.read<ModalsState>().add(
                    Padding(
                      padding: const EdgeInsets.all(20.0),
                      child: FractionallySizedBox(
                        widthFactor: 0.5,
                        heightFactor: 0.8,
                        child: ListView(children: [text]),
                      ),
                    ),
                  );
            },
            child: const Text(
              "Debug",
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ),
      ].map((element) => _wrap(element)).toList(),
    );
  }

  Widget _wrap(Widget widget) {
    return Expanded(
      child: Container(
        // TODO: shrink the ugly space between the buttons
        padding: const EdgeInsets.all(4),
        child: widget,
      ),
    );
  }
}
