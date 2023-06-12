import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../models/garden/bed.dart';
import '../../models/session.dart';
import '../wrappers/collapsible.dart';

class BedView extends StatelessWidget {
  final Bed bed;

  const BedView({super.key, required this.bed});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: Collapsible(
        header: BedViewHeader(bed: bed),
        child: BedViewContent(bed: bed),
      ),
    );
  }
}

class BedViewHeader extends StatefulWidget {
  const BedViewHeader({
    super.key,
    required this.bed,
  });

  final Bed bed;

  @override
  State<BedViewHeader> createState() => _BedViewHeaderState();
}

class _BedViewHeaderState extends State<BedViewHeader> {
  bool _editingName = false;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        ControlledTextInput(
          value: widget.bed.name,
          onChange: (newValue, transient) {
            context.read<SessionState>().editGarden(
                (garden) => garden.editBed(
                    widget.bed.id, (bed) => bed.rename(newValue)),
                transient: transient);
          },
          editing: _editingName,
          onEditingFinished: () {
            setState(() {
              _editingName = false;
            });
          },
        ),
        if (!_editingName)
          ElevatedButton(
              onPressed: () {
                setState(() {
                  _editingName = true;
                });
              },
              child: const Text("Edit"))
      ],
    );
  }
}

class BedViewContent extends StatelessWidget {
  const BedViewContent({
    super.key,
    required this.bed,
  });

  final Bed bed;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        ControlledTextInput(
          value: bed.name,
          onChange: (newValue, transient) {
            context.read<SessionState>().editGarden(
                (garden) =>
                    garden.editBed(bed.id, (bed) => bed.rename(newValue)),
                transient: transient);
          },
        ),
        ControlledTextInput(
          value: bed.name,
          onChange: (newValue, transient) {
            context.read<SessionState>().editGarden(
                (garden) =>
                    garden.editBed(bed.id, (bed) => bed.rename(newValue)),
                transient: transient);
          },
        )
      ],
    );
  }
}
