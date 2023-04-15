import 'dart:collection';
import 'dart:ffi';

class Garden {
  const Garden(this._beds, this._nursery);

  final List<Bed> _beds;
  UnmodifiableListView<Bed> get beds => UnmodifiableListView(_beds);

  final List<Plant> _nursery;
  UnmodifiableListView<Plant> get nursery => UnmodifiableListView(_nursery);
}

class Element<T> {
  const Element(this.id, this.x, this.y, this.element);

  final Int id;
  final Float x;
  final Float y;
  final T element;
}

class Plant {
  const Plant(this.id, this.name);

  final Int id;
  final String name;
}

class Bed {}

class PlantInstance {}

class Label {}

class Arrow {}
