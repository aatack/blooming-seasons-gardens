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
  final int availableId;

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
    this.availableId,
    this._images,
  );

  static Garden blank(String name) {
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
          id: availableId,
          origin: Point.blank(),
          name: "Bed $availableId",
        )
      ],
      nursery,
      background,
      availableId + 1,
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
        garden.availableId,
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
      availableId,
      images,
    );
  }

  Garden addInstance(int bedId,
      {Element? element, String? name, int? templateId}) {
    Bed update(Bed bed) {
      return bed.id == bedId
          ? Bed(
              [
                ...bed.instances,
                Instance(
                  id: availableId,
                  name:
                      name ?? "${element.runtimeType.toString()} $availableId",
                  position: Point.blank(),
                  element: element,
                  templateId: templateId,
                )
              ],
              id: bed.id,
              origin: bed.origin,
              name: bed.name,
            )
          : bed;
    }

    return Garden(
      this.name,
      _beds.map((bed) => update(bed)).toList(),
      update(nursery),
      background,
      availableId + 1,
      images,
    );
  }

  Garden editInstance(
      int id, Instance Function(Instance, List<CachedImage>) update,
      {List<CachedImage>? images}) {
    final parent = instanceParent(id);

    if (parent == nursery.id) {
      return withImages(images ?? [], (garden, newImages) {
        final newInstance = update(
            garden.nursery.instances
                .firstWhere((instance) => instance.id == id),
            newImages);

        return Garden(
          garden.name,
          garden.beds
              .map((bed) => bed.updateInstances((instance) =>
                  instance.templateId == id
                      ? instance.withElement(newInstance.element)
                      : instance))
              .toList(),
          garden.nursery.updateInstances(
              (instance) => instance.id == id ? newInstance : instance),
          garden.background,
          garden.availableId,
          garden.images,
        );
      });
    } else {
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
  }

  Garden removeInstance(int id) {
    final parent = instanceParent(id);

    if (parent == nursery.id) {
      return Garden(
        name,
        _beds
            .map((bed) => bed.updateInstances((instance) =>
                instance.templateId == id
                    ? instance.withTemplate(null)
                    : instance))
            .toList(),
        Bed(
          nursery.instances.where((instance) => instance.id != id).toList(),
          id: nursery.id,
          origin: nursery.origin,
          name: nursery.name,
        ),
        background,
        availableId,
        _images,
      );
    } else {
      return editBed(
        parent,
        (bed, _) => Bed(
          bed.instances.where((instance) => instance.id != id).toList(),
          id: bed.id,
          origin: bed.origin,
          name: bed.name,
        ),
      );
    }
  }

  int instanceParent(int instanceId) {
    for (final bed in [...beds, nursery]) {
      if (bed.instances.any((instance) => instance.id == instanceId)) {
        return bed.id;
      }
    }
    throw Exception("Could not find instance with ID $instanceId");
  }

  Garden withBackground(PositionedImage newBackground) {
    return Garden(name, _beds, nursery, newBackground, availableId, _images);
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
        availableId,
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
    "availableId": garden.availableId,
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
  final nursery = deserialiseBed(garden["nursery"], images);

  final beds =
      List<Bed>.from(garden["beds"].map((bed) => deserialiseBed(bed, images)));

  final background = PositionedImage.deserialise(garden["background"], images);

  return Garden(
      garden["name"], beds, nursery, background, garden["availableId"], images);
}
