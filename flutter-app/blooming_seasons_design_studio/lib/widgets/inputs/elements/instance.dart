import 'package:blooming_seasons_design_studio/models/modals.dart';
import 'package:blooming_seasons_design_studio/models/selections.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/elements/label.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/point.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:blooming_seasons_design_studio/widgets/screens/garden_view/editor/nursery_tab.dart';
import 'package:blooming_seasons_design_studio/widgets/top_down.dart';
import 'package:flutter/material.dart' hide Element;
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../models/garden/arrow.dart';
import '../../../models/garden/bed.dart';
import '../../../models/garden/instance.dart';
import '../../../models/garden/label.dart';
import '../../../models/garden/plant.dart';
import '../../../models/session.dart';
import '../../../models/structs/point.dart';
import '../../../theme.dart';
import '../../wrappers/hoverable.dart';
import '../button.dart';
import 'arrow.dart';
import 'plant.dart';

/// Context provided to an instance editor if it is being rendered in the garden.
///
/// Instance editors being rendered as part of the nursery do not have the same
/// context and so render less information.
@immutable
class BedContext {
  final Bed nursery;
  final int parentId;

  const BedContext(this.nursery, this.parentId);
}

class InstanceEditor extends StatefulWidget {
  final Instance instance;
  final Selections selections;
  final BedContext? bedContext;

  late final Element element;

  InstanceEditor(
      {super.key,
      required this.instance,
      required this.selections,
      this.bedContext}) {
    element = instance.element ??
        bedContext!.nursery.instanceMap[instance.templateId!]!.element!;
  }

  bool get expanded => selections.selected == instance.id;

  @override
  State<InstanceEditor> createState() => _InstanceEditorState();
}

class _InstanceEditorState extends State<InstanceEditor> {
  bool _editingName = false;

  @override
  Widget build(BuildContext context) {
    final colour = Colors.grey[100]!;
    final hoverColour = darker(colour, amount: 10);
    final clickColour = darker(colour, amount: 20);

    return Hoverable(
      onTap: () {
        final id =
            widget.expanded ? widget.bedContext?.parentId : widget.instance.id;
        context
            .read<SessionState>()
            .updateSelections((selections) => selections.withSelected(id));
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
                    if (widget.expanded) _body(context)
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

    if (widget.element is Plant) {
      icon = Icons.energy_savings_leaf_outlined;
    } else if (widget.element is Label) {
      icon = Icons.label_outline_sharp;
    } else if (widget.element is Arrow) {
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
                      (instance, _) => instance.withName(newValue),
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
              (instance, _) => instance.withPosition(newPosition),
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
        hidePosition: widget.bedContext == null,
      );
    } else if (widget.instance.element is Label) {
      content = LabelEditor(
        label: widget.instance.element as Label,
        setElement: setElement,
        position: position,
        setPosition: setPosition,
        hidePosition: widget.bedContext == null,
      );
    } else if (widget.instance.element is Arrow) {
      content = ArrowEditor(
        arrow: widget.instance.element as Arrow,
        setElement: setElement,
        position: position,
        setPosition: setPosition,
        hidePosition: widget.bedContext == null,
      );
    } else {
      content = Column(
        children: [
          FormLayout(
              children: pointInput(
                  label: "Position",
                  point: widget.instance.position,
                  setPoint: setPosition)),
          _templateSelection(
            context,
            widget
                .bedContext!.nursery.instanceMap[widget.instance.templateId!]!,
            widget.bedContext!.nursery,
          )
        ],
      );
    }

    return FormLayoutItem(child: content);
  }

  Widget _templateSelection(
      BuildContext context, Instance template, Bed nursery) {
    return Padding(
      padding: const EdgeInsets.only(top: 0, bottom: 0),
      child: Row(mainAxisSize: MainAxisSize.max, children: [
        _wrap(Button(
          onClicked: () {
            context.read<ModalsState>().add(NurseryModal(
                nursery: nursery,
                onSelect: (newTemplate) {
                  context.read<SessionState>().editGarden((garden) =>
                      garden.editInstance(
                          widget.instance.id,
                          (instance, _) =>
                              instance.withTemplate(newTemplate.id)));
                  context.read<ModalsState>().clear();
                }));
          },
          backgroundColour: Theme.of(context).colorScheme.surfaceVariant,
          child: Text("Template: ${template.name}"),
        )),
        _wrap(Button(
          onClicked: () {
            context.read<SessionState>().editGarden((garden) =>
                garden.editInstance(
                    widget.instance.id,
                    (instance, _) => instance.withElement(garden
                        .nursery.instanceMap[instance.templateId]!.element)));
          },
          backgroundColour: null,
          child: const Text("Disassociate"),
        )),
      ]),
    );
  }

  Widget _wrap(Widget widget) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(4),
        child: widget,
      ),
    );
  }
}

class InstancePainter extends Painter {
  final Instance instance;
  final Bed nursery;
  final Selections selections;

  // Whether or not the parent bed is hovered or selected
  final bool hovered;
  final bool selected;

  late final Offset _offset;
  late final Painter _child;
  late final Element _element;

  InstancePainter(this.instance, this.nursery, this.selections,
      {required this.hovered, required this.selected}) {
    _offset = instance.position.offset;
    _element =
        instance.element ?? nursery.instanceMap[instance.templateId!]!.element!;

    final instanceHovered = hovered ||
        (selections.hovered == instance.id) ||
        (instance.templateId != null &&
            selections.hovered == instance.templateId);
    final instanceSelected = selected ||
        (selections.selected == instance.id) ||
        (instance.templateId != null &&
            selections.selected == instance.templateId);

    if (_element is Plant) {
      _child = PlantPainter(_element as Plant,
          hovered: instanceHovered, selected: instanceSelected);
    } else if (_element is Arrow) {
      _child = ArrowPainter(_element as Arrow,
          hovered: instanceHovered, selected: instanceSelected);
    } else if (_element is Label) {
      _child = LabelPainter(_element as Label,
          hovered: instanceHovered, selected: instanceSelected);
    } else {
      _child = PainterGroup(Offset.zero, []);
    }
  }

  @override
  int? hitTest(Offset position) {
    return _child.hitTest(position - _offset);
  }

  @override
  void paint(Canvas canvas) {
    canvas.save();
    canvas.translate(_offset.dx, _offset.dy);

    _child.paint(canvas);

    canvas.restore();
  }
}

class InstanceSelector extends StatelessWidget {
  // Assumes that the passed instance does *not* use a template
  final Instance instance;
  final void Function() onClick;
  final bool divider;

  const InstanceSelector(
      {super.key,
      required this.instance,
      required this.onClick,
      this.divider = true});

  @override
  Widget build(BuildContext context) {
    // TODO: factor out commonalities with the editor above
    final colour = Colors.grey[100]!;
    final hoverColour = darker(colour, amount: 10);
    final clickColour = darker(colour, amount: 20);

    return Hoverable(
      onTap: onClick,
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
              if (divider) const Divider(height: 0),
              Padding(
                padding: const EdgeInsets.all(5),
                child: FormLayout(
                  children: [
                    _header(context, hovered),
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

    if (instance.element is Plant) {
      icon = Icons.energy_savings_leaf_outlined;
    } else if (instance.element is Label) {
      icon = Icons.label_outline_sharp;
    } else if (instance.element is Arrow) {
      icon = Icons.arrow_right_alt_sharp;
    } else {
      throw UnimplementedError();
    }

    return FormLayoutItem(
      label: Icon(icon),
      child: Stack(
        children: [
          ControlledTextInput(
            value: instance.name,
            onChange: (newValue, transient) {},
            editing: false,
            onEditingFinished: () {},
          ),
        ],
      ),
    );
  }
}
