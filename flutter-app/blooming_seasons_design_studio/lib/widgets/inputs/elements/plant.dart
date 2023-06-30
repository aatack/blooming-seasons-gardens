import 'package:blooming_seasons_design_studio/models/modals.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/button.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:flutter/material.dart' hide Element;
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

import '../../../models/garden/instance.dart';
import '../../../models/garden/plant.dart';
import '../../../models/structs/point.dart';

class PlantEditor extends StatelessWidget {
  final Plant plant;
  final void Function(Element, bool) setElement;

  final Point position;
  final void Function(Point, bool) setPosition;

  const PlantEditor({
    super.key,
    required this.plant,
    required this.setElement,
    required this.position,
    required this.setPosition,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        FormLayout(
          children: [
            FormLayoutItem(
              label: const Text("Diameter"),
              child: validatedTextInput(
                plant.diameter,
                (newDiameter, transient) {
                  setElement(plant.resize(newDiameter), transient);
                },
              ),
            ),
          ],
        ),
        _typeSelection(context),
      ],
    );
  }

  Widget _typeSelection(BuildContext context) {
    final fillSelected = plant.type == PlantType.fill;
    final imageSelected = plant.type == PlantType.image;

    return Padding(
      padding: const EdgeInsets.only(top: 0, bottom: 0),
      child: Row(mainAxisSize: MainAxisSize.max, children: [
        _wrap(Button(
          onClicked: () {
            if (fillSelected) {
              context.read<ModalsState>().add(
                    _PlantFillEditorModal(
                      fill: plant.fill,
                      setFill: (newFill) =>
                          setElement(plant.withFill(newFill), true),
                    ),
                  );
            } else {
              setElement(plant.withType(PlantType.fill), false);
            }
          },
          backgroundColour: plant.type == PlantType.fill
              ? Theme.of(context).colorScheme.surfaceVariant
              : null,
          child: Text(fillSelected ? "Edit fill" : "Use fill"),
        )),
        _wrap(Button(
          onClicked: () {
            if (imageSelected) {
            } else {
              setElement(plant.withType(PlantType.image), false);
            }
          },
          backgroundColour: plant.type == PlantType.image
              ? Theme.of(context).colorScheme.surfaceVariant
              : null,
          child: Text(imageSelected ? "Edit image" : "Use image"),
        )),
      ]),
    );
  }

  Widget _wrap(Widget widget) {
    return Expanded(
      child: Container(
        // TODO: shrink the ugly space between the buttons
        padding: const EdgeInsets.all(4),
        child: widget,
      ),
    );
  }

  Widget _imageEditor(BuildContext context) {
    return FormLayout(children: []);
  }
}

class _PlantFillEditorModal extends StatelessWidget {
  final PlantFill fill;
  final void Function(PlantFill) setFill;

  const _PlantFillEditorModal({required this.fill, required this.setFill});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(8),
      width: 400,
      color: Colors.grey[100],
      child: FormLayout(children: [
        FormLayoutItem(
          label: const Text("Thickness"),
          child: validatedTextInput(
            fill.thickness,
            (newThickness, transient) {
              setFill(
                PlantFill(
                  thickness: newThickness,
                  colour: fill.colour,
                ),
              );
            },
          ),
        ),
        FormLayoutItem(
          label: const Text("Colour"),
          child: ColorPicker(
            // STARTHERE: move this into a modal to only capture the final value
            pickerColor: fill.colour,
            onColorChanged: (newColour) {
              // setFill(PlantFill(thickness: fill.thickness, colour: newColour));
            },
            enableAlpha: false,
          ),
        ),
      ]),
    );
  }
}
