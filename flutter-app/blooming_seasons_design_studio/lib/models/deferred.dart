class Deferred<T> {
  T? value;
  Exception? error;
  bool loading = false;

  Deferred._(this.value, this.error, this.loading);

  factory Deferred.value(T value) {
    return Deferred._(value, null, false);
  }

  factory Deferred.error(Exception error) {
    return Deferred._(null, error, false);
  }

  factory Deferred.loading() {
    return Deferred._(null, null, true);
  }

  factory Deferred.empty() {
    return Deferred._(null, null, false);
  }
}
