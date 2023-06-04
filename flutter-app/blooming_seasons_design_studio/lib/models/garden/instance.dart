import 'package:blooming_seasons_design_studio/models/garden/arrow.dart';
import 'package:blooming_seasons_design_studio/models/garden/label.dart';
import 'package:blooming_seasons_design_studio/models/garden/plant.dart';
import 'package:flutter/material.dart' show immutable;
import 'package:image/image.dart' show Image;

abstract class Element {
  dynamic serialise(Map<int, dynamic> templates, Map<Image, int> images);
}

@immutable
class Instance<E extends Element> {
  final int id;
  final double x;
  final double y;
  final E element;
  final int? template;

  const Instance({
    required this.id,
    required this.x,
    required this.y,
    required this.element,
    required this.template,
  });
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

Instance deserialiseInstance(Map<String, dynamic> instance,
    Map<int, Element> templates, Map<int, Image> images) {
  int? template;
  Element element;

  if (instance.containsKey("template")) {
    template = instance["template"];
    element = templates[template!]!;
  } else {
    template = null;
    element = deserialiseElement(instance["element"], images);
  }

  return Instance(
    id: instance["id"],
    x: instance["x"],
    y: instance["y"],
    element: element,
    template: template,
  );
}

Element deserialiseElement(dynamic element, Map<int, Image> images) {
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
