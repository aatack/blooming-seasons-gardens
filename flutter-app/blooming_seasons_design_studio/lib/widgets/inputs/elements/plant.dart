import 'package:blooming_seasons_design_studio/images.dart';
import 'package:blooming_seasons_design_studio/models/inputs/validated.dart';
import 'package:blooming_seasons_design_studio/models/modals.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/button.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:flutter/material.dart' hide Element, Image;
import 'package:flutter/material.dart' as material;
import 'package:flutter/rendering.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import 'package:image/image.dart' show Image;
import 'dart:html' as html;

import '../../../models/garden/instance.dart';
import '../../../models/garden/plant.dart';
import '../../../models/structs/point.dart';
import '../point.dart';

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
            ...pointInput(
                label: "Position", point: position, setPoint: setPosition),
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
                          setElement(plant.withFill(newFill), false),
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
              context.read<ModalsState>().add(
                    _PlantImageEditorModal(
                      image: plant.image,
                      setImage: (newImage) =>
                          setElement(plant.withImage(newImage), false),
                    ),
                  );
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
}

class _PlantFillEditorModal extends StatefulWidget {
  final PlantFill fill;
  final void Function(PlantFill) setFill;

  const _PlantFillEditorModal({required this.fill, required this.setFill});

  @override
  State<_PlantFillEditorModal> createState() => _PlantFillEditorModalState();
}

class _PlantFillEditorModalState extends State<_PlantFillEditorModal> {
  late ValidatedDouble _thickness;
  late Color _colour;

  @override
  void initState() {
    super.initState();

    _thickness = widget.fill.thickness;
    _colour = widget.fill.colour;
  }

  @override
  Widget build(BuildContext context) {
    return _wrapInModal(
      context,
      FormLayout(
        children: [
          FormLayoutItem(
            label: const Text("Thickness"),
            child: validatedTextInput(
              _thickness,
              (newThickness, transient) {
                setState(() {
                  _thickness = newThickness;
                });
              },
            ),
          ),
          FormLayoutItem(
            label: const Text("Colour"),
            child: ColorPicker(
              pickerColor: _colour,
              onColorChanged: (newColour) {
                setState(() {
                  _colour = newColour;
                });
              },
              enableAlpha: false,
            ),
          ),
        ],
      ),
      () {
        widget.setFill(PlantFill(thickness: _thickness, colour: _colour));
      },
    );
  }
}

class _PlantImageEditorModal extends StatefulWidget {
  final PlantImage image;
  final void Function(PlantImage) setImage;

  const _PlantImageEditorModal({required this.image, required this.setImage});

  @override
  State<_PlantImageEditorModal> createState() => _PlantImageEditorModalState();
}

class _PlantImageEditorModalState extends State<_PlantImageEditorModal> {
  late Image? _image;
  late Point _position;
  late ValidatedDouble _scale;

  late material.Image? _test;

  @override
  void initState() {
    super.initState();

    _image = widget.image.image;
    _position = widget.image.position;
    _scale = widget.image.scale;

    _test = null;
  }

  @override
  Widget build(BuildContext context) {
    return _wrapInModal(
      context,
      FormLayout(
        children: [
          FormLayoutItem(
            label: const Text("Image"),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                _test == null
                    ? Button(
                        onClicked: () async {
                          final image = await uploadImage();

                          if (image != null) {
                            setState(() {
                              _test = deserialiseImage(image);
                            });
                          }
                        },
                        child: const Text("Upload image"),
                      )
                    : Button(
                        onClicked: () {
                          setState(() {
                            _test = null;
                          });
                        },
                        child: const Text("Reset image"),
                      ),
              ],
            ),
          ),
          ...pointInput(
            label: "Position",
            point: _position,
            setPoint: (newPosition, _) {
              setState(() {
                _position = newPosition;
              });
            },
          ),
          FormLayoutItem(
            label: const Text("Scale"),
            child: validatedTextInput(
              _scale,
              (newScale, transient) {
                setState(() {
                  _scale = newScale;
                });
              },
            ),
          ),
          if (_test != null)
            FormLayoutItem(child: SizedBox(width: 300, child: _test)),
        ],
      ),
      () {
        widget.setImage(
            PlantImage(image: _image, position: _position, scale: _scale));
      },
    );
  }
}

Widget _wrapInModal(
    BuildContext context, Widget modal, void Function() onConfirm) {
  return Container(
    padding: const EdgeInsets.all(8),
    width: 400,
    color: Colors.grey[100],
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        modal,
        Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            Button(
                onClicked: () {
                  context.read<ModalsState>().pop();
                },
                child: const Text("Cancel")),
            const SizedBox(width: 8),
            Button(
                onClicked: () {
                  onConfirm();
                  context.read<ModalsState>().pop();
                },
                child: const Text("Confirm")),
          ],
        ),
      ],
    ),
  );
}
