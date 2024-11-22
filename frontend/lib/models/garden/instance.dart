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
  final Element? element;
  final int? templateId;

  Instance({
    required this.id,
    required this.name,
    required this.position,
    required this.element,
    required this.templateId,
  }) {
    assert((element == null) != (templateId == null));
  }

  Instance withName(String newName) {
    return Instance(
      id: id,
      name: newName,
      position: position,
      element: element,
      templateId: templateId,
    );
  }

  Instance withPosition(Point newPosition) {
    return Instance(
      id: id,
      name: name,
      position: newPosition,
      element: element,
      templateId: templateId,
    );
  }

  Instance withElement(Element? newElement) {
    return Instance(
      id: id,
      name: name,
      position: position,
      element: newElement,
      templateId: null,
    );
  }

  Instance withTemplate(int? newTemplateId) {
    return Instance(
      id: id,
      name: name,
      position: position,
      element: null,
      templateId: newTemplateId,
    );
  }
}

dynamic serialiseInstance(Instance instance) {
  final Map<String, dynamic> result = {
    "id": instance.id,
    "name": instance.name,
    "position": instance.position.serialise(),
  };

  if (instance.templateId != null) {
    result["templateId"] = instance.templateId!;
  } else if (instance.element != null) {
    result["element"] = instance.element!.serialise();
  }

  return result;
}

Instance deserialiseInstance(
    Map<String, dynamic> instance, Map<int, CachedImage> images) {
  late final int? template;
  late final Element? element;

  if (instance.containsKey("templateId")) {
    template = instance["templateId"];
    element = null;
  } else {
    template = null;
    element = deserialiseElement(instance["element"], images);
  }

  return Instance(
    id: instance["id"],
    name: instance["name"],
    position: Point.deserialise(instance["position"]),
    element: element,
    templateId: template,
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
