import 'package:blooming_seasons_gardens/models/session.dart';
import 'package:blooming_seasons_gardens/models/structs/positioned_image.dart';
import 'package:blooming_seasons_gardens/widgets/inputs/positioned_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class BackgroundTab extends StatelessWidget {
  final PositionedImage background;

  const BackgroundTab({super.key, required this.background});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: FractionallySizedBox(
        heightFactor: 1.0,
        child: Card(
          shape: const RoundedRectangleBorder(borderRadius: BorderRadius.zero),
          color: Colors.grey[100],
          elevation: 0,
          margin: const EdgeInsets.all(0),
          child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: ListView(
              children: [
                PositionedImageInput(
                  image: background,
                  setImage: (newBackground, transient) {
                    /* TODO: this code could be made a lot cleaner if the `withImages`
                      method were modified to also take nulls in the list of images. */
                    if (newBackground.image != null &&
                        newBackground.image!.id == null) {
                      context.read<SessionState>().editGarden((garden) {
                        return garden.withImages(
                          [newBackground.image!],
                          (innerGarden, images) => innerGarden.withBackground(
                            PositionedImage(
                              image: images[0],
                              position: newBackground.position,
                              scale: newBackground.scale,
                            ),
                          ),
                        );
                      });
                    } else {
                      context.read<SessionState>().editGarden(
                          (garden) => garden.withBackground(newBackground),
                          transient: transient);
                    }
                  },
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}
