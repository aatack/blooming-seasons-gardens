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

  const Instance(this.id, this.x, this.y, this.element, this.template);
}

dynamic serialiseInstance(
  Instance instance,
  Map<int, dynamic> templates,
  Map<Image, int> images,
) {
  throw UnimplementedError();
}
