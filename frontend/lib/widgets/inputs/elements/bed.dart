import 'package:blooming_seasons_gardens/models/modals.dart';
import 'package:blooming_seasons_gardens/models/selections.dart';
import 'package:blooming_seasons_gardens/widgets/inputs/button.dart';
import 'package:blooming_seasons_gardens/widgets/inputs/elements/instance.dart';
import 'package:blooming_seasons_gardens/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_gardens/widgets/inputs/point.dart';
import 'package:blooming_seasons_gardens/widgets/inputs/text.dart';
import 'package:blooming_seasons_gardens/widgets/screens/garden_view/editor/nursery_tab.dart';
import 'package:blooming_seasons_gardens/widgets/top_down.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../models/garden/arrow.dart';
import '../../../models/garden/bed.dart';
import '../../../models/garden/label.dart';
import '../../../models/garden/plant.dart';
import '../../../models/session.dart';
import '../../../theme.dart';
import '../../wrappers/hoverable.dart';

class BedEditor extends StatefulWidget {
  final Bed bed;
  final Selections selections;
  /* The nursery is passed when the editor being rendered is *not* the nursery,
    and so the garden's nursery exists (and must be accessible for templates). */
  final Bed? nursery;

  const BedEditor(
      {super.key, required this.bed, required this.selections, this.nursery});

  bool get expanded =>
      selections.selected == bed.id ||
      bed.instanceMap.containsKey(selections.selected);

  @override
  State<BedEditor> createState() => _BedEditorState();
}

class _BedEditorState extends State<BedEditor> {
  bool _editingName = false;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        _header(context),
        if (widget.expanded) _content(context),
      ],
    );
  }

  Widget _header(BuildContext context) {
    final colourScheme = Theme.of(context).colorScheme;

    return Hoverable(
      onMouseEnter: () {
        context.read<SessionState>().updateSelections(
            (selections) => selections.withHovered(widget.bed.id));
      },
      onMouseLeave: () {
        context
            .read<SessionState>()
            .updateSelections((selections) => selections.withHovered(null));
      },
      builder: (context, localHovered, clicked) {
        // Don't highlight the bed, or show widgets, if one of its children is
        // being highlighted while it's open
        final hovered = ((widget.selections.hovered == widget.bed.id ||
                widget.bed.instanceMap.containsKey(widget.selections.hovered) &&
                    !widget.expanded) ||
            localHovered);

        return Card(
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
                    Icon(widget.expanded
                        ? Icons.arrow_drop_down
                        : Icons.arrow_right),
                    ControlledTextInput(
                      value: widget.bed.name,
                      onChange: (newValue, transient) {
                        context.read<SessionState>().editGarden(
                            (garden) => garden.editBed(widget.bed.id,
                                (bed, _) => bed.withName(newValue)),
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
                // Don't show the icons if the bed is hovered via a child
                if ((widget.selections.hovered == widget.bed.id) &&
                    !_editingName)
                  _overlayedIcons(context),
              ],
            ),
          ),
        );
      },
      onTap: () {
        context.read<SessionState>().updateSelections((selections) =>
            selections.withSelected(widget.expanded ? null : widget.bed.id));
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
    final bedContext = widget.nursery == null
        ? null
        : BedContext(widget.nursery!, widget.bed.id);

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
                key: Key(instance.id.toString()),
                instance: instance,
                selections: widget.selections,
                bedContext: bedContext)),
            Button(
                onClicked: () {
                  context.read<ModalsState>().add(AddElementModal(
                      bed: widget.bed, nursery: widget.nursery));
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
  final Bed? nursery;

  const AddElementModal({super.key, required this.bed, this.nursery});

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
              context.read<SessionState>().editGarden((garden) =>
                  garden.addInstance(bed.id, element: Plant.blank()));
            },
            child: const Text("Plant"),
          ),
          const SizedBox(height: 8),
          Button(
            onClicked: () {
              context.read<ModalsState>().pop();
              context.read<SessionState>().editGarden((garden) =>
                  garden.addInstance(bed.id, element: Label.blank()));
            },
            child: const Text("Label"),
          ),
          const SizedBox(height: 8),
          Button(
            onClicked: () {
              context.read<ModalsState>().pop();
              context.read<SessionState>().editGarden((garden) =>
                  garden.addInstance(bed.id, element: Arrow.blank()));
            },
            child: const Text("Arrow"),
          ),
          // Only show the nursery option if the garden is not null
          if (nursery != null) const SizedBox(height: 8),
          if (nursery != null)
            Button(
              onClicked: () {
                final modals = context.read<ModalsState>();
                modals.add(NurseryModal(
                  nursery: nursery!,
                  onSelect: (instance) {
                    context.read<SessionState>().editGarden((garden) =>
                        garden.addInstance(bed.id,
                            templateId: instance.id, name: instance.name));
                    context.read<ModalsState>().clear();
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
  final Bed nursery;
  final Selections selections;

  BedPainter(this.bed, this.nursery, this.selections)
      : super(
          bed.origin.offset,
          bed.instances
              .map(
                (instance) => InstancePainter(instance, nursery, selections,
                    selected: selections.selected == bed.id,
                    hovered: selections.hovered == bed.id),
              )
              .toList(),
        );
}
