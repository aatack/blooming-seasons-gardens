import 'package:blooming_seasons_design_studio/widgets/inputs/elements/label.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:blooming_seasons_design_studio/widgets/top_down.dart';
import 'package:flutter/material.dart' hide Element;
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../models/garden/arrow.dart';
import '../../../models/garden/instance.dart';
import '../../../models/garden/label.dart';
import '../../../models/garden/plant.dart';
import '../../../models/session.dart';
import '../../../models/structs/point.dart';
import '../../../theme.dart';
import '../../wrappers/hoverable.dart';
import 'arrow.dart';
import 'plant.dart';

class InstanceEditor extends StatefulWidget {
  final Instance instance;
  final bool hidePosition;

  const InstanceEditor(
      {super.key, required this.instance, this.hidePosition = false});

  @override
  State<InstanceEditor> createState() => _InstanceEditorState();
}

class _InstanceEditorState extends State<InstanceEditor> {
  bool _collapsed = true;
  bool _editingName = false;

  @override
  Widget build(BuildContext context) {
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
                child: FormLayout(
                  children: [
                    _header(context, hovered),
                    if (!_collapsed) _body(context)
                  ],
                ),
              )
            ],
          ),
        );
      },
    );
  }

  FormLayoutItem _header(BuildContext context, bool hovered) {
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

    return FormLayoutItem(
      label: Icon(icon),
      child: Stack(
        children: [
          ControlledTextInput(
            value: widget.instance.name,
            onChange: (newValue, transient) {
              context.read<SessionState>().editGarden(
                    (garden) => garden.editInstance(
                      widget.instance.id,
                      (instance, _) => instance.rename(newValue),
                    ),
                    transient: transient,
                  );
            },
            editing: _editingName,
            onEditingFinished: () {
              setState(() {
                _editingName = false;
              });
            },
          ),
          if (hovered && !_editingName) _overlayedIcons(context),
        ],
      ),
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
              context.read<SessionState>().editGarden(
                    (garden) => garden.removeInstance(widget.instance.id),
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

  FormLayoutItem _body(BuildContext context) {
    final Point position = widget.instance.position;

    void setPosition(Point newPosition, bool transient) {
      context.read<SessionState>().editGarden(
            (garden) => garden.editInstance(
              widget.instance.id,
              (instance, _) => instance.reposition(newPosition),
            ),
            transient: transient,
          );
    }

    void setElement(Element newElement, bool transient) {
      context.read<SessionState>().editGarden(
            (garden) => garden.editInstance(
              widget.instance.id,
              (instance, _) => instance.withElement(newElement),
            ),
            transient: transient,
          );
    }

    late final Widget content;
    if (widget.instance.element is Plant) {
      content = PlantEditor(
        plant: widget.instance.element as Plant,
        updateElement: (updatePlant, transient, {images}) {
          context.read<SessionState>().editGarden(
                (garden) => garden.editInstance(
                    widget.instance.id,
                    (instance, cachedImages) => instance.withElement(
                        updatePlant(instance.element as Plant, cachedImages)),
                    images: images),
                transient: transient,
              );
        },
        position: position,
        setPosition: setPosition,
        hidePosition: widget.hidePosition,
      );
    } else if (widget.instance.element is Label) {
      content = LabelEditor(
        label: widget.instance.element as Label,
        setElement: setElement,
        position: position,
        setPosition: setPosition,
        hidePosition: widget.hidePosition,
      );
    } else if (widget.instance.element is Arrow) {
      content = ArrowEditor(
        arrow: widget.instance.element as Arrow,
        setElement: setElement,
        position: position,
        setPosition: setPosition,
        hidePosition: widget.hidePosition,
      );
    } else {
      throw UnimplementedError();
    }

    return FormLayoutItem(child: content);
  }
}

class InstancePainter extends Painter {
  final Instance instance;

  InstancePainter(this.instance);

  @override
  int? hitTest(Offset position) {
    // TODO: implement hitTest
    throw UnimplementedError();
  }

  @override
  void paint(Canvas canvas) {
    // TODO: implement paint
  }
}
