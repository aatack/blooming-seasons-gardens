import 'package:blooming_seasons_design_studio/widgets/inputs/elements/label.dart';
import 'package:flutter/material.dart' hide Element;

import '../../../models/garden/arrow.dart';
import '../../../models/garden/instance.dart';
import '../../../models/garden/label.dart';
import '../../../models/garden/plant.dart';
import '../../../theme.dart';
import '../../wrappers/hoverable.dart';
import '../point.dart';
import 'arrow.dart';
import 'plant.dart';

class InstanceEditor extends StatefulWidget {
  final Instance<Element> instance;

  const InstanceEditor({super.key, required this.instance});

  @override
  State<InstanceEditor> createState() => _InstanceEditorState();
}

class _InstanceEditorState extends State<InstanceEditor> {
  bool _collapsed = true;

  @override
  Widget build(BuildContext context) {
    late final Widget content;

    if (widget.instance.element is Plant) {
      content = PlantEditor(plant: widget.instance.element as Plant);
    } else if (widget.instance.element is Label) {
      content = LabelEditor(label: widget.instance.element as Label);
    } else if (widget.instance.element is Arrow) {
      content = ArrowEditor(arrow: widget.instance.element as Arrow);
    } else {
      throw UnimplementedError();
    }

    final colour = Colors.grey[100]!;
    final hoverColour = darker(colour, amount: 10);
    final clickColour = darker(colour, amount: 20);

    return Hoverable(
      onTap: () {
        setState(() {
          _collapsed = !_collapsed;
        });
      },
      builder: (context, hovered, clicked) {
        return Container(
          color: clicked
              ? clickColour
              : hovered
                  ? hoverColour
                  : colour,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Divider(height: 0),
              Padding(
                padding: const EdgeInsets.all(5),
                child: Table(
                  columnWidths: {
                    0: IntrinsicColumnWidth(),
                    1: IntrinsicColumnWidth(),
                    2: FlexColumnWidth()
                  },
                  defaultVerticalAlignment: TableCellVerticalAlignment.middle,
                  children: [
                    _header(context, hovered),
                    if (!_collapsed) _contentWrapper(context)
                  ],
                ),
              )
            ],
          ),
        );
      },
    );
  }

  TableRow _header(BuildContext context, bool hovered) {
    late final IconData icon;

    if (widget.instance.element is Plant) {
      icon = Icons.energy_savings_leaf_outlined;
    } else if (widget.instance.element is Label) {
      icon = Icons.label_outline_sharp;
    } else if (widget.instance.element is Arrow) {
      icon = Icons.arrow_right_alt_sharp;
    } else {
      throw UnimplementedError();
    }

    return TableRow(
      children: [
        TableCell(
          child: Icon(icon),
        ),
        const TableCell(child: SizedBox(width: 10)),
        TableCell(
          child: Stack(
            children: [
              Text(widget.instance.name),
              if (hovered) _overlayedIcons(context),
            ],
          ),
        ),
      ],
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

  TableRow _contentWrapper(BuildContext context) {
    return TableRow(
      children: [
        TableCell(
          child: Stack(children: []),
        ),
        const TableCell(child: SizedBox(width: 10)),
        TableCell(child: _contentInner(context)),
      ],
    );
  }

  Widget _contentInner(BuildContext context) {
    return PointInput(
        point: widget.instance.position, onChange: (newPosition, transient) {});
  }
}