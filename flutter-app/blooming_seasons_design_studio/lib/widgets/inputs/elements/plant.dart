import 'package:blooming_seasons_design_studio/images.dart';
import 'package:blooming_seasons_design_studio/models/inputs/validated.dart';
import 'package:blooming_seasons_design_studio/models/modals.dart';
import 'package:blooming_seasons_design_studio/models/structs/positioned_image.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/button.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/form_layout.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/positioned_image.dart';
import 'package:blooming_seasons_design_studio/widgets/inputs/text.dart';
import 'package:flutter/material.dart' hide Element, Image;
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

import '../../../models/garden/plant.dart';
import '../../../models/selections.dart';
import '../../../models/structs/point.dart';
import '../../top_down.dart';
import '../../wrappers/modals.dart';
import '../point.dart';

class PlantEditor extends StatelessWidget {
  final Plant plant;
  final void Function(Plant Function(Plant, List<CachedImage>), bool,
      {List<CachedImage>? images}) updateElement;

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
                      (element, _) => element.withDiameter(newDiameter),
                      transient);
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
                      diameter: plant.diameter,
                      image: plant.image,
                      setImage: (newImage) {
                        if (newImage.image != null &&
                            newImage.image!.id == null) {
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
                            images: [newImage.image!],
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
    return wrapInModal(
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
        ), onConfirm: () {
      closeModal(context);
      widget.setFill(PlantFill(thickness: _thickness, colour: _colour));
    }, onCancel: () {
      closeModal(context);
    });
  }
}

class _PlantImageEditorModal extends StatefulWidget {
  final ValidatedDouble diameter;
  final PositionedImage image;
  final void Function(PositionedImage) setImage;

  const _PlantImageEditorModal(
      {required this.diameter, required this.image, required this.setImage});

  @override
  State<_PlantImageEditorModal> createState() => _PlantImageEditorModalState();
}

class _PlantImageEditorModalState extends State<_PlantImageEditorModal> {
  late PositionedImage _image;

  @override
  void initState() {
    super.initState();

    _image = widget.image;
  }

  @override
  Widget build(BuildContext context) {
    final transformedPosition = _transform(_image);

    return wrapInModal(
      context,
      Column(
        children: [
          PositionedImageInput(
            image: _image,
            setImage: (newImage, _) {
              setState(() {
                if (newImage.image == null) {
                  _image = newImage;
                } else {
                  /* Reset the scales to sensible values, putting the reticle
                    approximately in the middle of the image.
                    
                    NOTE: this isn't quite accurate, as the scale appears to
                    be a little on the small side.  It's not quite clear
                    exactly why this is.  Furthermore, setting the scale and
                    position via the text boxes doesn't work as intended. */
                  final approximateScale =
                      widget.diameter.output / newImage.image!.image.width;

                  _image = PositionedImage(
                    image: newImage.image,
                    position: Point(
                      ValidatedDouble.initialise(-0.5 *
                          newImage.image!.image.width *
                          approximateScale),
                      ValidatedDouble.initialise(-0.5 *
                          newImage.image!.image.height *
                          approximateScale),
                    ),
                    scale: newImage.scale,
                  );
                }
              });
            },
          ),
          /* TODO: validate the scale as strictly greater than, instead of 
            greater than or equal to. */
          if (_image.image != null && _image.scale.output > 0)
            Padding(
              padding: const EdgeInsets.all(12.0),
              child: ClipRect(
                child: SizedBox(
                  width: _PreviewPainter.size,
                  height: _PreviewPainter.size,
                  child: TopDown(
                    position: transformedPosition,
                    setPosition: (newPosition) {
                      setState(() {
                        _image = _inverseTransform(newPosition, _image.image);
                      });
                    },
                    child: _PreviewPainter(_image.image, transformedPosition),
                  ),
                ),
              ),
            ),
        ],
      ),
      onConfirm: () {
        closeModal(context);
        widget.setImage(_image);
      },
      onCancel: () {
        closeModal(context);
      },
    );
  }

  TopDownPosition _transform(PositionedImage position) {
    /* Converts the image's transform to a reticle transform.
    
      To derive this, consider the position and size in pixel space (ie. where
      each pixel of the image is one unit) of both the clip path and the
      reticle.  Note that both must be equal; from this set of equalities, the
      relationship between the two transforms can be calculated. */

    final scale = (2 * _PreviewPainter.reticleRadius * position.scale.output) /
        widget.diameter.output;

    final x = _PreviewPainter.reticleCentre.dx +
        ((scale / position.scale.output) * position.position.x.output);
    final y = _PreviewPainter.reticleCentre.dy +
        ((scale / position.scale.output) * position.position.y.output);

    return TopDownPosition(x, y, scale);
  }

  PositionedImage _inverseTransform(
      TopDownPosition position, CachedImage? image) {
    final scale = (position.scale * widget.diameter.output) /
        (2 * _PreviewPainter.reticleRadius);

    final x = (scale / position.scale) *
        (position.x - _PreviewPainter.reticleCentre.dx);
    final y = (scale / position.scale) *
        (position.y - _PreviewPainter.reticleCentre.dy);

    return PositionedImage(
        image: image,
        position:
            Point(ValidatedDouble.initialise(x), ValidatedDouble.initialise(y)),
        scale: ValidatedDouble.initialise(scale));
  }
}

class _PreviewPainter extends Painter {
  static const double size = 300; // Width and height of the preview
  static const Offset reticleCentre = Offset(size / 2, size / 2);
  static const double reticleRadius = size / 3;

  final CachedImage? image;
  final TopDownPosition position;

  late final Painter _imagePainter;

  _PreviewPainter(this.image, this.position) {
    _imagePainter = PositionedImagePainter(
      PositionedImage(
        image: image,
        position: Point.blank(),
        scale: ValidatedDouble.initialise(1),
      ),
    );
  }

  @override
  int? hitTest(Offset position) {
    return null;
  }

  @override
  void paint(Canvas canvas) {
    _imagePainter.paint(canvas);

    final outline = Paint()
      ..color = Colors.black
      ..style = PaintingStyle.stroke
      ..strokeWidth = position.worldDistance(3);

    canvas.drawCircle(
      position.worldPosition(reticleCentre),
      position.worldDistance(reticleRadius),
      outline,
    );
  }
}

class PlantPainter extends Painter {
  static const centre = Offset.zero;

  final Plant plant;

  // Whether the instance or its parent bed is hovered or selected
  final bool hovered;
  final bool selected;

  late final Paint _outlinePaint;
  late final Paint _fillPaint;
  late final Path _clipPath;

  late final double _radius;

  late final PositionedImagePainter _imagePainter;

  PlantPainter(this.plant, {required this.hovered, required this.selected}) {
    _outlinePaint = Paint()
      ..color = Colors.black
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    _fillPaint = Paint()
      ..color = plant.fill.colour
      ..style = PaintingStyle.fill;

    _radius = plant.diameter.output * 0.5;

    _imagePainter = PositionedImagePainter(plant.image);

    _clipPath = Path()
      ..addOval(Rect.fromCircle(center: Offset.zero, radius: _radius));
  }

  @override
  void paint(Canvas canvas) {
    if (plant.type == PlantType.fill) {
      canvas.drawCircle(Offset.zero, _radius, _outlinePaint);
      canvas.drawCircle(Offset.zero, _radius, _fillPaint);
    } else {
      canvas.save();
      canvas.clipPath(_clipPath);

      _imagePainter.paint(canvas);

      canvas.restore();
    }
  }

  @override
  int? hitTest(Offset position) {
    return null;
  }
}
