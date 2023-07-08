import 'package:flutter/material.dart' show immutable;

import '../../images.dart';
import '../structs/point.dart';
import 'arrow.dart';
import 'label.dart';
import 'plant.dart';

enum ElementType { plant, label, arrow }

abstract class Element {
  dynamic serialise();
}

@immutable
class Instance {
  final int id;
  final String name;
  final Point position;
  final Element element;
  final int? templateID;

  const Instance({
    required this.id,
    required this.name,
    required this.position,
    required this.element,
    required this.templateID,
  });

  Instance rename(String newName) {
    return Instance(
      id: id,
      name: newName,
      position: position,
      element: element,
      templateID: templateID,
    );
  }

  Instance reposition(Point newPosition) {
    return Instance(
      id: id,
      name: name,
      position: newPosition,
      element: element,
      templateID: templateID,
    );
  }

  Instance withElement(Element newElement) {
    return Instance(
      id: id,
      name: name,
      position: position,
      element: newElement,
      templateID: templateID,
    );
  }
}

dynamic serialiseInstance(Instance instance) {
  final Map<String, dynamic> result = {
    "id": instance.id,
    "name": instance.name,
    "position": instance.position.serialise(),
  };

  if (instance.templateID != null) {
    result["templateID"] = instance.templateID!;
  } else {
    result["element"] = instance.element.serialise();
  }

  return result;
}

Instance deserialiseInstance(
  Map<String, dynamic> instance,
  Map<int, Element> templates,
  Map<int, CachedImage> images,
) {
  late int? template;
  late Element element;

  if (instance.containsKey("templateID")) {
    template = instance["templateID"];
    element = templates[template!]!;
  } else {
    template = null;
    element = deserialiseElement(instance["element"], images);
  }

  return Instance(
    id: instance["id"],
    name: instance["name"],
    position: Point.deserialise(instance["position"]),
    element: element,
    templateID: template,
  );
}

Element deserialiseElement(dynamic element, Map<int, CachedImage> images) {
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
