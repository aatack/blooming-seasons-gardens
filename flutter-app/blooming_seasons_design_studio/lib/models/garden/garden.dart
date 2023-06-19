import 'dart:collection';
import 'dart:convert';

import 'package:blooming_seasons_design_studio/models/garden/arrow.dart';
import 'package:blooming_seasons_design_studio/models/garden/label.dart';
import 'package:blooming_seasons_design_studio/models/garden/plant.dart';
import 'package:flutter/material.dart' show Colors, immutable;
import 'package:image/image.dart' show Image;

import '../inputs/validated.dart';
import '../structs/point.dart';
import 'bed.dart';
import 'instance.dart';

@immutable
class Garden {
  final String name;

  final List<Bed> _beds;
  UnmodifiableListView<Bed> get beds => UnmodifiableListView(_beds);

  // Maps identifiers to a template associated with that identifier
  final Map<int, Element> _templates;
  UnmodifiableMapView<int, Element> get templates =>
      UnmodifiableMapView(_templates);

  // The next available identifier for elements in the garden
  final int availableID;

  const Garden(this.name, this._beds, this._templates, this.availableID);

  factory Garden.blank(String name) {
    return Garden(name, const [], const {}, 0);
  }

  Garden addBed() {
    return Garden(
      name,
      [
        ...beds,
        Bed(
          const [],
          id: availableID,
          origin: const Point(ValidatedDouble("0"), ValidatedDouble("0")),
          name: "Bed $availableID",
        )
      ],
      templates,
      availableID + 1,
    );
  }

  Garden editBed(int id, Bed Function(Bed) update) {
    return Garden(
      name,
      _beds.map((bed) => bed.id == id ? update(bed) : bed).toList(),
      _templates,
      availableID,
    );
  }

  Garden deleteBed(int id) {
    return Garden(
      name,
      _beds.where((bed) => bed.id != id).toList(),
      _templates,
      availableID,
    );
  }

  Garden addElement(int bedID, Element element) {
    return Garden(
      name,
      _beds
          .map((bed) => bed.id == bedID
              ? Bed([
                  ...bed.elements,
                  Instance(
                    id: availableID,
                    position:
                        const Point(ValidatedDouble("0"), ValidatedDouble("0")),
                    element: element,
                    templateID: null,
                  )
                ], id: bed.id, origin: bed.origin, name: bed.name)
              : bed)
          .toList(),
      _templates,
      availableID + 1,
    );
  }
}

/// Return a JSON-compatible representation of the garden.
dynamic serialiseGarden(Garden garden) {
  final Map<int, dynamic> templates = {};
  final Map<Image, int> images = {};

  final List<dynamic> beds =
      garden.beds.map((bed) => serialiseBed(bed, templates, images)).toList();

  return {
    "name": garden.name,
    "beds": beds,
    "templates":
        templates.map((id, template) => MapEntry(id.toString(), template)),
    "availableID": garden.availableID,
    "images": images.map((image, id) => MapEntry(id, _serialiseImage(image))),
  };
}

/// Produce a garden object from its JSON representation.
///
/// The format of the passed object should mirror that of the return format
/// of the `serialise` function.
Garden deserialiseGarden(dynamic garden) {
  final images = Map<int, Image>.from(
    garden["images"].map(
      (id, image) => MapEntry(id, _deserialiseImage(image)),
    ),
  );

  final templates = Map<int, Element>.from(
    garden["templates"].map(
      (id, template) => MapEntry(
        int.parse(id),
        deserialiseElement(template, images),
      ),
    ),
  );

  final beds = List<Bed>.from(
      garden["beds"].map((bed) => deserialiseBed(bed, templates, images)));

  return Garden(garden["name"], beds, templates, garden["availableID"]);
}

dynamic _serialiseImage(Image image) {
  return {
    "data": base64.encode(image.getBytes()),
    "width": image.width,
    "height": image.height,
  };
}

Image _deserialiseImage(dynamic image) {
  return Image.fromBytes(
    width: image["width"],
    height: image["height"],
    bytes: base64.decode(image["data"]).buffer,
  );
}
