import 'package:flutter/material.dart';

@immutable
class ImmutableLinkedList<Data> {
  final Data first;
  final ImmutableLinkedList<Data>? rest;

  const ImmutableLinkedList({required this.first, required this.rest});
}

ImmutableLinkedList<Data> cons<Data>(
    Data first, ImmutableLinkedList<Data>? rest) {
  return ImmutableLinkedList(first: first, rest: rest);
}
