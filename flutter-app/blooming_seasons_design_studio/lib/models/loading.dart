import 'package:flutter_bloc/flutter_bloc.dart';

class Loading extends Cubit<String?> {
  Loading() : super(null);

  void setLoading(String message) {
    emit(message);
  }

  void setFinished() {
    emit(null);
  }
}
