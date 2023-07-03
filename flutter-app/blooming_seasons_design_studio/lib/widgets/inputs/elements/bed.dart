import 'package:blooming_seasons_design_studio/models/modals.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/button.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/elements/instance.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/point.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:blooming_seasons_design_studio/widgets/screens/garden_view/editor/nursery_tab.dart';
import 'package:blooming_seasons_design_studio/widgets/top_down.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../models/garden/arrow.dart';
import '../../../models/garden/bed.dart';
import '../../../models/garden/garden.dart';
import '../../../models/garden/label.dart';
import '../../../models/garden/plant.dart';
import '../../../models/session.dart';
import '../../../theme.dart';
import '../../wrappers/hoverable.dart';

class BedEditor extends StatefulWidget {
  final Bed bed;
  final Garden? garden;

  const BedEditor({super.key, required this.bed, this.garden});

  @override
  State<BedEditor> createState() => _BedEditorState();
}

class _BedEditorState extends State<BedEditor> {
  bool _editingName = false;
  bool _collapsed = true;

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
                              widget.bed.id, (bed, _) => bed.rename(newValue)),
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
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            FormLayout(
              children: pointInput(
                label: "Origin",
                point: widget.bed.origin,
                setPoint: (newOrigin, transient) {
                  context.read<SessionState>().editGarden(
                        (garden) => garden.editBed(
                          widget.bed.id,
                          (bed, _) => Bed(
                            widget.bed.instances,
                            id: widget.bed.id,
                            origin: newOrigin,
                            name: widget.bed.name,
                          ),
                        ),
                        transient: transient,
                      );
                },
              ),
            ),
            const SizedBox(height: 8),
            ...widget.bed.instances.map((instance) => InstanceEditor(
                key: Key(instance.id.toString()), instance: instance)),
            Button(
                onClicked: () {
                  context.read<ModalsState>().add(
                      AddElementModal(bed: widget.bed, garden: widget.garden));
                },
                child: const Text("Add element")),
          ],
        ),
      ),
    );
  }
}

class AddElementModal extends StatelessWidget {
  final Bed bed;
  final Garden? garden;

  const AddElementModal({super.key, required this.bed, this.garden});

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
                  (garden) => garden.addInstance(bed.id, Plant.blank()));
            },
            child: const Text("Plant"),
          ),
          const SizedBox(height: 8),
          Button(
            onClicked: () {
              context.read<ModalsState>().pop();
              context.read<SessionState>().editGarden(
                  (garden) => garden.addInstance(bed.id, Label.blank()));
            },
            child: const Text("Label"),
          ),
          const SizedBox(height: 8),
          Button(
            onClicked: () {
              context.read<ModalsState>().pop();
              context.read<SessionState>().editGarden(
                  (garden) => garden.addInstance(bed.id, Arrow.blank()));
            },
            child: const Text("Arrow"),
          ),
          if (garden != null) const SizedBox(height: 8),
          if (garden != null)
            Button(
              onClicked: () {
                final modals = context.read<ModalsState>();
                modals.add(NurseryModal(
                  garden: garden!,
                  onSelect: (instance) {
                    modals.clear();
                    // TODO: add a new instance to the current bed
                  },
                  onCancel: () {
                    modals.pop();
                  },
                ));
              },
              child: const Text("Nursery"),
            ),
        ],
      ),
    );
  }
}

class BedPainter extends PainterGroup {
  final Bed bed;

  BedPainter(this.bed)
      : super(
          bed.origin.offset,
          bed.instances
              .map(
                (instance) => InstancePainter(instance),
              )
              .toList(),
        );
}
