import 'dart:convert';
import 'dart:typed_data';

import 'package:blooming_seasons_design_studio/images.dart';
import 'package:blooming_seasons_design_studio/models/inputs/validated.dart';
import 'package:blooming_seasons_design_studio/models/modals.dart';
import 'package:blooming_seasons_design_studio/models/structs/positioned_image.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/button.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:flutter/material.dart' hide Element, Image;
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import 'dart:ui' as ui;

import '../../../models/garden/plant.dart';
import '../../../models/structs/point.dart';
import '../../top_down.dart';
import '../point.dart';

class PlantEditor extends StatelessWidget {
  final Plant plant;
  final void Function(Plant Function(Plant, List<CachedImage>), bool,
      {List<String>? images}) updateElement;

  final Point position;
  final void Function(Point, bool) setPosition;

  final bool hidePosition;

  const PlantEditor({
    super.key,
    required this.plant,
    required this.updateElement,
    required this.position,
    required this.setPosition,
    this.hidePosition = false,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        FormLayout(
          children: [
            if (!hidePosition)
              ...pointInput(
                  label: "Position", point: position, setPoint: setPosition),
            FormLayoutItem(
              label: const Text("Diameter"),
              child: validatedTextInput(
                plant.diameter,
                (newDiameter, transient) {
                  updateElement(
                      (element, _) => element.resize(newDiameter), transient);
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
                      setFill: (newFill) => updateElement(
                          (element, _) => element.withFill(newFill), false),
                    ),
                  );
            } else {
              updateElement(
                  (element, _) => element.withType(PlantType.fill), false);
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
                      setImage: (newImage) {
                        if (newImage.image?.id == -1) {
                          // A new image has been added, and must be cached
                          return updateElement(
                            (element, cachedImages) => element.withImage(
                              PositionedImage(
                                image: cachedImages[0],
                                position: newImage.position,
                                scale: newImage.scale,
                              ),
                            ),
                            false,
                            images: [newImage.image!.string],
                          );
                        } else {
                          return updateElement(
                              (element, _) => element.withImage(newImage),
                              false);
                        }
                      },
                    ),
                  );
            } else {
              updateElement(
                  (element, _) => element.withType(PlantType.image), false);
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
  final PositionedImage image;
  final void Function(PositionedImage) setImage;

  const _PlantImageEditorModal({required this.image, required this.setImage});

  @override
  State<_PlantImageEditorModal> createState() => _PlantImageEditorModalState();
}

class _PlantImageEditorModalState extends State<_PlantImageEditorModal> {
  late CachedImage? _image;

  late Point _position;
  late ValidatedDouble _scale;

  @override
  void initState() {
    super.initState();

    _image = widget.image.image;
    _position = widget.image.position;
    _scale = widget.image.scale;
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
                _image == null
                    ? Button(
                        onClicked: () async {
                          final image = await uploadImage();

                          if (image != null) {
                            setState(() {
                              /* At this point, the change has not yet been
                                committed; so we don't want to cache the image
                                in the garden yet.  Instead we save its ID as
                                -1, to denote that a change in the image has
                                occurred. */
                              _image = CachedImage.deserialise(-1, image);
                            });
                          }
                        },
                        child: const Text("Upload image"),
                      )
                    : Button(
                        onClicked: () {
                          setState(() {
                            _image = null;
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
          if (_image != null)
            FormLayoutItem(
              child: SizedBox(width: 300, child: _image!.image),
            ),
        ],
      ),
      () {
        widget.setImage(
          PositionedImage(image: _image, position: _position, scale: _scale),
        );
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

class PlantPainter extends Painter {
  static const centre = Offset.zero;

  final Plant plant;

  late final Paint _outlinePaint;
  late final Paint _fillPaint;

  late final double _radius;

  ui.Image? _image;

  PlantPainter(this.plant) {
    _outlinePaint = Paint()
      ..color = Colors.black
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    _fillPaint = Paint()
      ..color = plant.fill.colour
      ..style = PaintingStyle.fill;

    _radius = plant.diameter.output * 0.5;

    if (plant.type == PlantType.image && plant.image.image != null) {
      final image = plant.image.image!;
      final codec = ui.instantiateImageCodec(
        Uint8List.fromList(base64.decode(image.string)),
        targetHeight: image.image.height?.toInt(),
        targetWidth: image.image.width?.toInt(),
      );
      codec.then((value) => value.getNextFrame().then((value) {
            _image = value.image;
          }));
    }
  }

  @override
  void paint(Canvas canvas) {
    if (plant.type == PlantType.fill) {
      canvas.drawCircle(Offset.zero, _radius, _outlinePaint);
      canvas.drawCircle(Offset.zero, _radius, _fillPaint);
    } else if (_image != null) {
      canvas.drawImage(_image!, Offset.zero, Paint());
    }
  }

  @override
  int? hitTest(Offset position) {
    return null;
  }
}
