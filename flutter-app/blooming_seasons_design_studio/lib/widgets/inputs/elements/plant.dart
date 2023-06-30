import 'package:blooming_seasons_design_studio/widgets/inputs/button.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:flutter/material.dart' hide Element;
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
        if (plant.type == PlantType.fill) _fillEditor(context),
        if (plant.type == PlantType.image) _imageEditor(context),
      ],
    );
  }

  Widget _typeSelection(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 0, bottom: 0),
      child: Row(mainAxisSize: MainAxisSize.max, children: [
        _wrap(Button(
          onClicked: () {
            setElement(plant.withType(PlantType.fill), true);
          },
          backgroundColour: plant.type == PlantType.fill
              ? Theme.of(context).colorScheme.surfaceVariant
              : null,
          child: const Text("Fill"),
        )),
        _wrap(Button(
          onClicked: () {
            setElement(plant.withType(PlantType.image), true);
          },
          backgroundColour: plant.type == PlantType.image
              ? Theme.of(context).colorScheme.surfaceVariant
              : null,
          child: const Text("Image"),
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

  Widget _fillEditor(BuildContext context) {
    return FormLayout(children: [
      FormLayoutItem(
        label: const Text("Thickness"),
        child: validatedTextInput(
          plant.fill.thickness,
          (newThickness, transient) {
            setElement(
              plant.withFill(PlantFill(
                thickness: newThickness,
                colour: plant.fill.colour,
              )),
              transient,
            );
          },
        ),
      ),
      FormLayoutItem(
        label: const Text("Colour"),
        child: ColorPicker(
          pickerColor: plant.fill.colour,
          onColorChanged: (newColour) {},
          pickerAreaHeightPercent: 0.35,
          enableAlpha: false,
        ),
      ),
    ]);
  }

  Widget _imageEditor(BuildContext context) {
    return FormLayout(children: []);
  }
}
