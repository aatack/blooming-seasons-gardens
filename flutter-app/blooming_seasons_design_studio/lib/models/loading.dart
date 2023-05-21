import 'package:flutter_bloc/flutter_bloc.dart';

class LoadingState extends Cubit<String?> {
  LoadingState() : super(null);

  void setLoading(String message) {
    emit(message);
  }

  void setFinished() {
    emit(null);
  }
}
