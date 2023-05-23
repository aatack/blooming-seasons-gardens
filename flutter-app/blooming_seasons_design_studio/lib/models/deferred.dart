enum _State {
  data,
  error,
  loading,
  empty,
}

class Deferred<Data> {
  Data? _data;
  Object? _error;
  _State _state;

  Deferred._(this._data, this._error, this._state);

  factory Deferred.data(Data data) {
    return Deferred._(data, null, _State.data);
  }

  factory Deferred.error(Object error) {
    return Deferred._(null, error, _State.error);
  }

  factory Deferred.loading() {
    return Deferred._(null, null, _State.loading);
  }

  factory Deferred.empty() {
    return Deferred._(null, null, _State.empty);
  }

  Result handle<Result>({
    required Result Function(Data) data,
    required Result Function(Object) error,
    required Result Function() loading,
    required Result Function() empty,
  }) {
    switch (_state) {
      case _State.data:
        return data(_data!);
      case _State.error:
        return error(_error!);
      case _State.loading:
        return loading();
      case _State.empty:
        return empty();
    }
  }
}

Future<void> populate<Data>({
  required Future<Data> Function() get,
  required void Function(Deferred<Data>) set,
}) async {
  set(Deferred.loading());

  try {
    final data = await get();
    set(Deferred.data(data));
  } catch (error) {
    set(Deferred.error(error));
  }
}
