import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'models/session.dart';
import 'widgets/app.dart';
import 'widgets/wrappers/modals.dart';

void main() {
  runApp(const AppWrapper());
}

class AppWrapper extends StatelessWidget {
  const AppWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Blooming Seasons Design Studio",
      home: BlocProvider<SessionState>(
        create: (_) {
          final state = SessionState();
          state.loadGardens();
          return state;
        },
        child: const Scaffold(
          body: ModalsWrapper(
            child: App(),
          ),
        ),
      ),
    );
  }
}
