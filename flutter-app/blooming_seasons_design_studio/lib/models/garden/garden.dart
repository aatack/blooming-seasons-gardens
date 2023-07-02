import 'dart:collection';

import 'package:flutter/material.dart' show immutable;

import '../../images.dart';
import '../structs/point.dart';
import '../structs/positioned_image.dart';
import 'bed.dart';
import 'instance.dart';

@immutable
class Garden {
  final String name;

  final List<Bed> _beds;
  UnmodifiableListView<Bed> get beds => UnmodifiableListView(_beds);

  // Contains template elements that can be reused throughout the garden
  final Bed nursery;

  final PositionedImage background;

  // The next available identifier for elements in the garden
  final int availableID;

  /* Images are stored in the backend as JSON strings, which is horribly
    inefficient but makes for an easier server overall.  A consequence of
    this is that loading images, and converting them to widgets, is a bit
    too slow to do individually for every garden element as we would with
    any other data structure.
    
    To accelerate it, images are cached when they are first added to the
    garden (see the `withImages` function), and then loaded from that
    cache by their IDs when each element is deserialised.  This makes it
    quick enough to at least be acceptable. */
  final Map<int, CachedImage> _images;
  UnmodifiableMapView<int, CachedImage> get images =>
      UnmodifiableMapView(_images);

  const Garden(
    this.name,
    this._beds,
    this.nursery,
    this.background,
    this.availableID,
    this._images,
  );

  factory Garden.blank(String name) {
    return Garden(
      name,
      const [],
      Bed(
        const [],
        id: -1,
        origin: Point.blank(),
        name: "nursery",
      ),
      PositionedImage.blank(),
      0,
      const {},
    );
  }

  Garden addBed() {
    return Garden(
      name,
      [
        ...beds,
        Bed(
          const [],
          id: availableID,
          origin: Point.blank(),
          name: "Bed $availableID",
        )
      ],
      nursery,
      background,
      availableID + 1,
      images,
    );
  }

  Garden editBed(int id, Bed Function(Bed, List<CachedImage>) update,
      {List<CachedImage>? images}) {
    return withImages(
      images ?? [],
      (garden, cachedImages) => Garden(
        garden.name,
        garden.beds
            .map((bed) => bed.id == id ? update(bed, cachedImages) : bed)
            .toList(),
        id == garden.nursery.id
            ? update(garden.nursery, cachedImages)
            : garden.nursery,
        garden.background,
        garden.availableID,
        garden.images,
      ),
    );
  }

  Garden deleteBed(int id) {
    return Garden(
      name,
      _beds.where((bed) => bed.id != id).toList(),
      nursery,
      background,
      availableID,
      images,
    );
  }

  Garden addInstance(int bedID, Element element) {
    Bed update(Bed bed) {
      return bed.id == bedID
          ? Bed(
              [
                ...bed.instances,
                Instance(
                  id: availableID,
                  name: "${element.runtimeType.toString()} $availableID",
                  position: Point.blank(),
                  element: element,
                  templateID: null,
                )
              ],
              id: bed.id,
              origin: bed.origin,
              name: bed.name,
            )
          : bed;
    }

    return Garden(
      name,
      _beds.map((bed) => update(bed)).toList(),
      update(nursery),
      background,
      availableID + 1,
      images,
    );
  }

  Garden editInstance(
      int id, Instance Function(Instance, List<CachedImage>) update,
      {List<CachedImage>? images}) {
    return editBed(
      instanceParent(id),
      (bed, cachedImages) => Bed(
        bed.instances
            .map((instance) =>
                instance.id == id ? update(instance, cachedImages) : instance)
            .toList(),
        id: bed.id,
        origin: bed.origin,
        name: bed.name,
      ),
      images: images,
    );
  }

  Garden removeInstance(int id) {
    return editBed(
      instanceParent(id),
      (bed, _) => Bed(
        bed.instances.where((instance) => instance.id != id).toList(),
        id: bed.id,
        origin: bed.origin,
        name: bed.name,
      ),
    );
  }

  int instanceParent(int instanceID) {
    for (final bed in [...beds, nursery]) {
      if (bed.instances.any((instance) => instance.id == instanceID)) {
        return bed.id;
      }
    }
    throw Exception("Could not find instance with ID $instanceID");
  }

  /// Cache an image, then update the garden with the resulting image ID.
  Garden withImages(List<CachedImage> newImages,
      Garden Function(Garden, List<CachedImage>) update) {
    final Map<int, CachedImage> cachedImageRepository = Map.from(images);
    final List<CachedImage> cachedImageArguments = [];

    overNewImages:
    for (final image in newImages) {
      for (final cachedImage in cachedImageRepository.values) {
        if (cachedImage.string == image.string) {
          cachedImageArguments.add(cachedImage);
          continue overNewImages;
        }
      }

      final entry =
          CachedImage(cachedImageRepository.length, image.string, image.image);
      cachedImageRepository[entry.id!] = entry;
      cachedImageArguments.add(entry);
    }

    return update(
      Garden(
        name,
        _beds,
        nursery,
        background,
        availableID,
        cachedImageRepository,
      ),
      cachedImageArguments,
    );
  }
}

/// Return a JSON-compatible representation of the garden.
dynamic serialiseGarden(Garden garden) {
  final nursery = serialiseBed(garden.nursery);
  final List<dynamic> beds =
      garden.beds.map((bed) => serialiseBed(bed)).toList();

  final background = garden.background.serialise();

  return {
    "name": garden.name,
    "beds": beds,
    "nursery": nursery,
    "background": background,
    "availableID": garden.availableID,
    "images": garden.images
        .map((id, image) => MapEntry(id.toString(), image.serialise())),
  };
}

/// Produce a garden object from its JSON representation.
///
/// The format of the passed object should mirror that of the return format
/// of the `serialise` function.
Future<Garden> deserialiseGarden(dynamic garden) async {
  // Something to do with this being async prevents it from being written as
  // a map; not quite sure what
  final Map<int, CachedImage> images = {};
  for (final MapEntry<String, dynamic> entry in garden["images"].entries) {
    final id = int.parse(entry.key);
    final image = await CachedImage.deserialise(id, entry.value);
    images[id] = image;
  }

  // Elements in the nursery should never themselves utilise the nursery
  final nursery = deserialiseBed(garden["nursery"], {}, images);

  final Map<int, Element> templates = Map.fromEntries(nursery.instances
      .map((instance) => MapEntry(instance.id, instance.element)));

  final beds = List<Bed>.from(
      garden["beds"].map((bed) => deserialiseBed(bed, templates, images)));

  final background = PositionedImage.deserialise(garden["background"], images);

  return Garden(
      garden["name"], beds, nursery, background, garden["availableID"], images);
}
