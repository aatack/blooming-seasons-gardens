import 'package:blooming_seasons_design_studio/widgets/providers/modals.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'models/garden.dart' show GardenState;
import 'models/session.dart';
import 'widgets/app.dart';

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
          state.loadAvailableGardens();
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
