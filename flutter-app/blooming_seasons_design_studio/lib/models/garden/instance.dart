import 'package:blooming_seasons_design_studio/models/garden/arrow.dart';
import 'package:blooming_seasons_design_studio/models/garden/label.dart';
import 'package:blooming_seasons_design_studio/models/garden/plant.dart';
import 'package:flutter/material.dart' show immutable;
import 'package:image/image.dart' show Image;

abstract class GardenElement {
  dynamic serialise(Map<int, dynamic> templates, Map<Image, int> images);
}

abstract class BedElement implements GardenElement {}

@immutable
class Instance<E extends GardenElement> {
  final int id;
  final double x;
  final double y;
  final E element;
  final int? template;

  const Instance({required this.id, required this.x, required this.y, required this.element, required this.template,});
}

dynamic serialiseInstance(
  Instance instance,
  Map<int, dynamic> templates,
  Map<Image, int> images,
) {
  final dynamic result = {
    "id": instance.id,
    "x": instance.x,
    "y": instance.y,
  };

  if (instance.template != null) {
    if (!templates.containsKey(instance.template!)) {
      templates[instance.template!] =
          instance.element.serialise(templates, images);
    }

    result["template"] = instance.template!;
  } else {
    result["element"] = instance.element.serialise(templates, images);
  }

  return result;
}

Instance<E> deserialiseInstance<E extends GardenElement>(dynamic instance) {
  return Instance(
    id: instance["id"],
    x: instance["x"],
    y: instance["y"],
    element: instance["template"], // TODO: properly deserialise
    template: instance["template"],
  )
}

BedElement deserialiseBedElement(dynamic element, Map<int, Image> images) {
  final elementType = element["elementType"];

  switch (elementType) {
    case "plant":
      return deserialisePlant(element, images);
    case "label":
      return deserialiseLabel(element);
    case "arrow":
      return deserialiseArrow(element);
    default:
      throw Exception("Unrecognised bed element type: $elementType");
  }
}
