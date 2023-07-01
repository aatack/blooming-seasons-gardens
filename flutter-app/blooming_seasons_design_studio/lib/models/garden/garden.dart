import 'dart:collection';

import 'package:flutter/material.dart' show immutable;

import '../structs/point.dart';
import 'bed.dart';
import 'instance.dart';

@immutable
class Garden {
  final String name;

  final List<Bed> _beds;
  UnmodifiableListView<Bed> get beds => UnmodifiableListView(_beds);

  // Contains template elements that can be reused throughout the garden
  final Bed nursery;

  // The next available identifier for elements in the garden
  final int availableID;

  const Garden(this.name, this._beds, this.nursery, this.availableID);

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
        0);
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
      availableID + 1,
    );
  }

  Garden editBed(int id, Bed Function(Bed) update) {
    return Garden(
      name,
      _beds.map((bed) => bed.id == id ? update(bed) : bed).toList(),
      id == nursery.id ? update(nursery) : nursery,
      availableID,
    );
  }

  Garden deleteBed(int id) {
    return Garden(
      name,
      _beds.where((bed) => bed.id != id).toList(),
      nursery,
      availableID,
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
      availableID + 1,
    );
  }

  Garden editInstance(int id, Instance Function(Instance) update) {
    return editBed(
      instanceParent(id),
      (bed) => Bed(
        bed.instances
            .map((instance) => instance.id == id ? update(instance) : instance)
            .toList(),
        id: bed.id,
        origin: bed.origin,
        name: bed.name,
      ),
    );
  }

  Garden removeInstance(int id) {
    return editBed(
      instanceParent(id),
      (bed) => Bed(
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
}

/// Return a JSON-compatible representation of the garden.
dynamic serialiseGarden(Garden garden) {
  final Map<String, int> images = {};

  final nursery = serialiseBed(garden.nursery, images);
  final List<dynamic> beds =
      garden.beds.map((bed) => serialiseBed(bed, images)).toList();

  return {
    "name": garden.name,
    "beds": beds,
    "nursery": nursery,
    "availableID": garden.availableID,
    "images": images.map((image, id) => MapEntry(id.toString(), image)),
  };
}

/// Produce a garden object from its JSON representation.
///
/// The format of the passed object should mirror that of the return format
/// of the `serialise` function.
Garden deserialiseGarden(dynamic garden) {
  final images = Map<int, String>.from(
    garden["images"].map(
      (id, image) => MapEntry(int.parse(id), image),
    ),
  );

  // Elements in the nursery should never themselves utilise the nursery
  final nursery = deserialiseBed(garden["nursery"], {}, images);

  final Map<int, Element> templates = Map.fromEntries(nursery.instances
      .map((instance) => MapEntry(instance.id, instance.element)));

  final beds = List<Bed>.from(
      garden["beds"].map((bed) => deserialiseBed(bed, templates, images)));

  return Garden(garden["name"], beds, nursery, garden["availableID"]);
}
