import 'package:blooming_seasons_gardens/models/structs/positioned_image.dart';
import 'package:flutter/material.dart';

import '../../images.dart';
import 'button.dart';
import 'form_layout.dart';
import 'point.dart';
import 'text.dart';

class PositionedImageInput extends StatelessWidget {
  final PositionedImage image;
  final void Function(PositionedImage, bool) setImage;

  const PositionedImageInput(
      {super.key, required this.image, required this.setImage});

  @override
  Widget build(BuildContext context) {
    return FormLayout(
      children: [
        FormLayoutItem(
          label: const Text("Image"),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              image.image == null
                  ? Button(
                      onClicked: () async {
                        final upload = await uploadImage();

                        if (upload != null) {
                          setImage(
                              PositionedImage(
                                  image: upload,
                                  position: image.position,
                                  scale: image.scale),
                              false);
                        }
                      },
                      child: const Text("Upload image"),
                    )
                  : Button(
                      onClicked: () {
                        setImage(
                            PositionedImage(
                                image: null,
                                position: image.position,
                                scale: image.scale),
                            false);
                      },
                      child: const Text("Reset image"),
                    ),
            ],
          ),
        ),
        ...pointInput(
          label: "Position",
          point: image.position,
          setPoint: (newPosition, transient) {
            setImage(
                PositionedImage(
                    image: image.image,
                    position: newPosition,
                    scale: image.scale),
                transient);
          },
        ),
        FormLayoutItem(
          label: const Text("Scale"),
          child: validatedTextInput(
            image.scale,
            (newScale, transient) {
              setImage(
                  PositionedImage(
                      image: image.image,
                      position: image.position,
                      scale: newScale),
                  transient);
            },
          ),
        ),
        // TODO: include a preview of the plant
      ],
    );
  }
}
