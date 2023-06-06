import 'package:flutter/material.dart';

import 'linked_list.dart';

// NOTE: if this becomes a performance bottleneck, it can very easily be
//       replaced with a linked list

@immutable
class History<Data> {
  final ImmutableLinkedList<Data>? past;

  /// The checkpoint is the last state that will be included in the history.
  ///
  /// This is useful for making small, transient changes that do not need to
  /// be recovered later.  Such changes will be made to the present object,
  /// which is still the main source of information contained in the history
  /// object.  Whenever a change is made, the checkpoint will be added to the
  /// history instead of the present object.  If no transient changes have
  /// been made, the two will be the same and so it will make no difference.
  final Data checkpoint;

  final Data present;

  final ImmutableLinkedList<Data>? future;

  const History(this.past, this.checkpoint, this.present, this.future);

  factory History.from(Data data) {
    return History(null, data, data, null);
  }

  bool get canGoBack => past != null;
  bool get canGoForward => future != null;

  /// Commit a new piece of data to history.
  ///
  /// If the current state is not the head, any future values will be
  /// overwritten by this operation.
  ///
  /// When `transient` is set to `true`, the current state will be updated
  /// but not added to the history.  If the history is later stepped back,
  /// this piece of data will be ignored, and it will proceed to the most
  /// recent non-transient commit instead.
  History<Data> commit(Data data, {bool transient = false}) {
    return History(
        cons(checkpoint, past), transient ? checkpoint : data, data, null);
  }

  /// Step back in the version history, if possible.
  ///
  /// If stepping back is not possible, gives the same object back.
  History<Data> back() {
    if (canGoBack) {
      return this;
    } else {
      return History(
          past!.rest, past!.first, past!.first, cons(checkpoint, future));
    }
  }

  /// Step forward in the version history, if possible.
  ///
  /// If stepping forward is not possible, gives the same object back.
  History<Data> forward() {
    if (canGoForward) {
      return this;
    } else {
      return History(
          cons(checkpoint, past), future!.first, future!.first, future!.rest);
    }
  }
}
