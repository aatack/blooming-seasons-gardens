import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../models/garden/bed.dart';
import '../../../models/garden/garden.dart';
import '../../../models/modals.dart';
import '../../../models/session.dart';
import '../../elements/bed_view.dart';
import '../../inputs/button.dart';
import '../../wrappers/resizable.dart';

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
              HeaderButtons(garden: garden),
              BedsView(beds: garden.beds)
            ],
          ),
        ),
      ),
    );
  }
}

class HeaderButtons extends StatelessWidget {
  final Garden garden;

  const HeaderButtons({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Button(
          onClicked: () {
            context
                .read<SessionState>()
                .editGarden((garden) => garden.addNewBed());
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
            "Undo",
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
        Button(
          onClicked: () {
            context.read<SessionState>().redo();
          },
          child: const Text(
            "Redo",
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
        Button(
          onClicked: () {
            const encoder = JsonEncoder.withIndent("  ");

            final text = Text(
              encoder.convert(serialiseGarden(garden)),
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
      ].map((element) => wrap(element)).toList(),
    );
  }

  Widget wrap(Widget widget) {
    return Expanded(
      child: Container(
        // TODO: shrink the ugly space between the buttons
        padding: const EdgeInsets.all(4),
        child: widget,
      ),
    );
  }
}

class BedsView extends StatelessWidget {
  final List<Bed> beds;

  const BedsView({super.key, required this.beds});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: FractionallySizedBox(
        heightFactor: 1.0,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(8.0, 4.0, 8.0, 0.0),
          child: ListView(
            children: beds.map((bed) => BedView(bed: bed)).toList(),
          ),
        ),
      ),
    );
  }
}
