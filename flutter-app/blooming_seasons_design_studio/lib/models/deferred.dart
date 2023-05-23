class Deferred<Data> {
  Data? _value;
  Object? _error;
  bool _loading = false;

  Deferred._(this._value, this._error, this._loading);

  factory Deferred.value(Data value) {
    return Deferred._(value, null, false);
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
    required Result Function(Data) value,
    required Result Function(Object) error,
    required Result Function() loading,
    required Result Function() empty,
  }) {
    if (_value != null) {
      return value(_value!);
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
    set(Deferred.value(data));
  } catch (error) {
    set(Deferred.error(error));
  }
}
