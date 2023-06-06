import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../models/garden/bed.dart';
import '../../../models/garden/garden.dart';
import '../../../models/session.dart';
import '../../elements/bed.dart';
import '../../wrappers/collapsible.dart';
import '../../wrappers/resizable.dart';

class Editor extends StatelessWidget {
  final Garden garden;

  const Editor({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    return FractionallySizedBox(
      child: Resizable(
        initialWidth: 200,
        child: Container(
          color: Colors.white,
          child: Column(
            children: [const HeaderButtons(), BedsView(beds: garden.beds)],
          ),
        ),
      ),
    );
  }
}

class HeaderButtons extends StatelessWidget {
  const HeaderButtons({super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        ElevatedButton(
          onPressed: () {
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
        ElevatedButton(
          onPressed: () {},
          child: const Text(
            "Templates",
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
    return Column(
      children: beds.map((bed) => BedView(bed: bed)).toList(),
    );
  }
}
