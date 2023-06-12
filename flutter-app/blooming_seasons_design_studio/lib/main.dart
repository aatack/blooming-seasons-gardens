import 'package:blooming_seasons_design_studio/theme.dart';
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
      theme: ThemeData(
        colorScheme: lightColorScheme,
        textTheme: const TextTheme(
          bodyMedium: TextStyle(
            fontFamily: "Spectral",
          ),
          labelLarge: TextStyle(
            fontFamily: "Spectral",
          ),
          titleMedium: TextStyle(
            fontFamily: "Spectral",
          ),
        ),
      ),
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
