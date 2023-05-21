import 'package:flutter_bloc/flutter_bloc.dart';

class Loading extends Cubit<bool> {
  Loading() : super(false);

  void setLoading() {
    emit(true);
  }

  void setNotLoading() {
    emit(false);
  }
}
