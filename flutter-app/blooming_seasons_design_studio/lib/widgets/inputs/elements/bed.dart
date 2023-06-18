import 'package:blooming_seasons_design_studio/models/modals.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/button.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/point.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../models/garden/bed.dart';
import '../../../models/garden/instance.dart';
import '../../../models/session.dart';
import '../../../theme.dart';
import '../../wrappers/hoverable.dart';

class BedEditor extends StatefulWidget {
  final Bed bed;

  const BedEditor({super.key, required this.bed});

  @override
  State<BedEditor> createState() => _BedEditorState();
}

class _BedEditorState extends State<BedEditor> {
  bool _editingName = false;
  bool _collapsed = false;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        _header(context),
        if (!_collapsed) _content(context),
      ],
    );
  }

  Widget _header(BuildContext context) {
    final colourScheme = Theme.of(context).colorScheme;

    return Hoverable(
      builder: (context, hovered, clicked) => Card(
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.zero),
        color: clicked
            ? darker(darker(colourScheme.surfaceVariant))
            : (hovered
                ? darker(colourScheme.surfaceVariant)
                : colourScheme.surfaceVariant),
        margin: const EdgeInsets.all(0),
        child: SizedBox(
          height: 36,
          child: Stack(
            alignment: Alignment.centerLeft,
            children: [
              Row(
                children: [
                  Icon(_collapsed ? Icons.arrow_drop_down : Icons.arrow_right),
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
                ],
              ),
              if (hovered && !_editingName) _overlayedIcons(context),
            ],
          ),
        ),
      ),
      onTap: () {
        setState(() {
          _collapsed = !_collapsed;
        });
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
            icon: Icons.add_circle,
            height: 20,
            onTap: () {
              context
                  .read<ModalsState>()
                  .add(_AddElementModal(bed: widget.bed));
            },
            colour: colour,
            hoverColour: hoverColour,
            clickColour: clickColour,
          ),
          const SizedBox(width: 8),
          HoverableIcon(
            icon: Icons.edit,
            height: 20,
            onTap: () {
              setState(() {
                _editingName = true;
              });
            },
            colour: colour,
            hoverColour: hoverColour,
            clickColour: clickColour,
          ),
          const SizedBox(width: 8),
          HoverableIcon(
            icon: Icons.delete,
            height: 20,
            onTap: () {
              context
                  .read<SessionState>()
                  .editGarden((garden) => garden.deleteBed(widget.bed.id));
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

  Widget _content(BuildContext context) {
    return Card(
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.zero),
      color: Colors.grey[100],
      elevation: 0,
      margin: const EdgeInsets.all(0),
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            PointInput(
              point: widget.bed.origin,
              onChange: (newOrigin, transient) {
                context.read<SessionState>().editGarden(
                      (garden) => garden.editBed(
                        widget.bed.id,
                        (bed) => Bed(
                          widget.bed.elements,
                          id: widget.bed.id,
                          origin: newOrigin,
                          name: widget.bed.name,
                        ),
                      ),
                      transient: transient,
                    );
              },
            ),
          ],
        ),
      ),
    );
  }
}

class _AddElementModal extends StatelessWidget {
  final Bed bed;

  const _AddElementModal({required this.bed});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Button(
            onClicked: () {
              context.read<ModalsState>().pop();
              context.read<SessionState>().editGarden(
                  (garden) => garden.addElement(bed.id, ElementType.plant));
            },
            child: const Text("Plant"),
          ),
          const SizedBox(height: 8),
          Button(
            onClicked: () {
              context.read<ModalsState>().pop();
              context.read<SessionState>().editGarden(
                  (garden) => garden.addElement(bed.id, ElementType.label));
            },
            child: const Text("Label"),
          ),
          const SizedBox(height: 8),
          Button(
            onClicked: () {
              context.read<ModalsState>().pop();
              context.read<SessionState>().editGarden(
                  (garden) => garden.addElement(bed.id, ElementType.arrow));
            },
            child: const Text("Arrow"),
          ),
        ],
      ),
    );
  }
}
