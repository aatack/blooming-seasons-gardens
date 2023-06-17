import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../models/garden/bed.dart';
import '../../models/session.dart';
import '../inputs/button.dart';
import 'package:blooming_seasons_design_studio/theme.dart';

import '../../models/modals.dart';
import '../wrappers/hoverable.dart';

class BedView extends StatefulWidget {
  final Bed bed;

  const BedView({super.key, required this.bed});

  @override
  State<BedView> createState() => _BedViewState();
}

class _BedViewState extends State<BedView> {
  final double height = 20;

  bool _editingName = false;
  bool _collapsed = false;

  @override
  Widget build(BuildContext context) {
    final colourScheme = Theme.of(context).colorScheme;

    return Hoverable(
      builder: (context, hovered, clicked) => Card(
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.zero),
        color: clicked
            ? darker(darker(colourScheme.surfaceVariant))
            : (hovered
                ? darker(colourScheme.surfaceVariant)
                : colourScheme.surfaceVariant),
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: SizedBox(
            height: height,
            child: Stack(
              children: [
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    widget.bed.name,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                if (hovered) _overlayedIcons(context),
              ],
            ),
          ),
        ),
      ),
      onTap: () {
        context
            .read<SessionState>()
            .loadGarden(widget.bed.name, context.read<ModalsState>());
      },
    );
  }

  Widget _overlayedIcons(BuildContext context) {
    final colour = Theme.of(context).colorScheme.onSurfaceVariant;
    final hoverColour = lighter(colour, amount: 50);
    final clickColour = lighter(colour, amount: 100);

    return Align(
      alignment: Alignment.centerRight,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          HoverableIcon(
            icon: Icons.edit,
            height: height,
            onTap: () {
              throw UnimplementedError();
            },
            colour: colour,
            hoverColour: hoverColour,
            clickColour: clickColour,
          ),
          const SizedBox(width: 8),
          HoverableIcon(
            icon: Icons.delete,
            height: height,
            onTap: () {
              context.read<ModalsState>().confirm(
                    message: "Delete garden ${widget.bed.name}?",
                    action: () {
                      context.read<SessionState>().deleteGarden(
                            widget.bed.name,
                            context.read<ModalsState>(),
                          );
                    },
                  );
            },
            colour: colour,
            hoverColour: hoverColour,
            clickColour: clickColour,
          ),
          const SizedBox(width: 8),
        ],
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
  final double height = 20;

  bool _editingName = false;
  bool _collapsed = false;

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
        Button(
          onClicked: () {
            setState(() {
              _editingName = true;
            });
          },
          child: const Text("Edit"),
        )
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
