import 'package:flutter/material.dart';

enum _State {
  data,
  error,
  loading,
  empty,
}

@immutable
class Thunk<Data> {
  final Data? _data;
  final Object? _error;
  final _State _state;

  const Thunk._(this._data, this._error, this._state);

  factory Thunk.data(Data data) {
    return Thunk._(data, null, _State.data);
  }

  factory Thunk.error(Object error) {
    return Thunk._(null, error, _State.error);
  }

  factory Thunk.loading() {
    return const Thunk._(null, null, _State.loading);
  }

  factory Thunk.empty() {
    return const Thunk._(null, null, _State.empty);
  }

  get isEmpty => _state == _State.empty;

  Result handle<Result>({
    required Result Function(Data) data,
    required Result Function(Object) error,
    required Result Function() loading,
    Result Function()? empty,
  }) {
    switch (_state) {
      case _State.data:
        return data(_data!);
      case _State.error:
        return error(_error!);
      case _State.loading:
        return loading();
      case _State.empty:
        if (empty != null) {
          return empty();
        } else {
          return error("Tried to handle an empty thunk");
        }
    }
  }

  static Future<void> populate<Data>({
    required Future<Data> Function() get,
    required void Function(Thunk<Data>) set,
  }) async {
    set(Thunk.loading());

    try {
      final data = await get();
      set(Thunk.data(data));
    } catch (error) {
      set(Thunk.error(error));
    }
  }
}
