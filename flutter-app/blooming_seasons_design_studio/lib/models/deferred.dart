class Deferred<Data> {
  Data? _data;
  Object? _error;
  bool _loading = false;

  Deferred._(this._data, this._error, this._loading);

  factory Deferred.data(Data data) {
    return Deferred._(data, null, false);
  }

  factory Deferred.error(Object error) {
    return Deferred._(null, error, false);
  }

  factory Deferred.loading() {
    return Deferred._(null, null, true);
  }

  factory Deferred.empty() {
    return Deferred._(null, null, false);
  }

  Result handle<Result>({
    required Result Function(Data) data,
    required Result Function(Object) error,
    required Result Function() loading,
    required Result Function() empty,
  }) {
    if (_data != null) {
      return data(_data!);
    } else if (_error != null) {
      return error(_error!);
    } else if (_loading) {
      return loading();
    } else {
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
