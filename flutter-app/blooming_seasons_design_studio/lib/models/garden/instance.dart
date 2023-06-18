import 'package:flutter/material.dart' show immutable;
import 'package:image/image.dart' show Image;

import 'arrow.dart';
import 'label.dart';
import 'plant.dart';

enum ElementType { plant, label, arrow }

abstract class Element {
  dynamic serialise(Map<int, dynamic> templates, Map<Image, int> images);
}

@immutable
class Instance<E extends Element> {
  final int id;
  final double x;
  final double y;
  final E element;
  final int? templateID;

  const Instance({
    required this.id,
    required this.x,
    required this.y,
    required this.element,
    required this.templateID,
  });
}

dynamic serialiseInstance(
  Instance instance,
  Map<int, dynamic> templates,
  Map<Image, int> images,
) {
  final Map<String, dynamic> result = {
    "id": instance.id,
    "x": instance.x,
    "y": instance.y,
  };

  if (instance.templateID != null) {
    if (!templates.containsKey(instance.templateID!)) {
      templates[instance.templateID!] =
          instance.element.serialise(templates, images);
    }

    result["template"] = instance.templateID!;
  } else {
    result["element"] = instance.element.serialise(templates, images);
  }

  return result;
}

Instance deserialiseInstance(Map<String, dynamic> instance,
    Map<int, Element> templates, Map<int, Image> images) {
  int? template;
  Element element;

  if (instance.containsKey("templateID")) {
    template = instance["templateID"];
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
    templateID: template,
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
