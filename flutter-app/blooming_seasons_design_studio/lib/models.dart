import 'dart:collection';
import 'dart:ffi';

class Garden {
  const Garden(this._beds, this._nursery);

  final List<Bed> _beds;
  UnmodifiableListView<Bed> get beds => UnmodifiableListView(_beds);

  final List<Template> _nursery;
  UnmodifiableListView<Template> get nursery => UnmodifiableListView(_nursery);
}

class Element<T> {
  const Element(this.id, this.x, this.y, this.element);

  final Int id;
  final Float x;
  final Float y;
  final T element;
}

class Template {
  const Template(this.id, this.plant);

  final Int id;
  final Plant plant;
}

class Bed {
  const Bed(this._elements);

  final List<Element> _elements;
  UnmodifiableListView<Element> get elements => UnmodifiableListView(_elements);
}

class Plant {
  const Plant(this.name);

  final String name;
}

class Label {
  const Label(this.text);

  final String text;
}

class Arrow {
  const Arrow(this.x, this.y);

  final Float x;
  final Float y;
}
