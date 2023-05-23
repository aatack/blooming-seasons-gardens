import 'package:flutter_bloc/flutter_bloc.dart';

import 'garden.dart';
import 'deferred.dart';

class SessionState extends Cubit<Session> {
  SessionState() : super(Session(Deferred.empty(), Deferred.empty()));
}

class Session {
  final Deferred<List<String>> availableGardens;
  final Deferred<Garden> currentGarden;

  const Session(this.availableGardens, this.currentGarden);
}
