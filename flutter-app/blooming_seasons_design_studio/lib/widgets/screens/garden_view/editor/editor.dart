import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../../models/garden/garden.dart';
import '../../../../models/modals.dart';
import '../../../../models/session.dart';
import '../../../inputs/button.dart';
import '../../../wrappers/resizable.dart';
import 'garden_tab.dart';

class Editor extends StatelessWidget {
  final Garden garden;

  const Editor({super.key, required this.garden});

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
              _TabButtons(garden: garden),
              GardenTab(beds: garden.beds)
            ],
          ),
        ),
      ),
    );
  }
}

class _TabButtons extends StatelessWidget {
  final Garden garden;

  const _TabButtons({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Button(
          onClicked: () {
            context
                .read<SessionState>()
                .editGarden((garden) => garden.addBed());
          },
          child: const Text(
            "New bed",
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
        Button(
          onClicked: () {
            context.read<SessionState>().undo();
          },
          child: const Text(
            "Nursery",
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
        Button(
          onClicked: () {
            print(serialiseGarden(
                context.read<SessionState>().state.garden.unpack()!.present));
          },
          child: const Text(
            "Background",
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
        Button(
          onClicked: () {
            const encoder = JsonEncoder.withIndent("  ");

            final serialisation = serialiseGarden(garden);
            serialisation["images"] = serialisation["images"].map((id, image) =>
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
