import 'package:blooming_seasons_design_studio/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'models/session.dart';
import 'widgets/app.dart';
import 'widgets/wrappers/hoverable.dart';
import 'widgets/wrappers/modals.dart';

void main() {
  runApp(const AppWrapper());
}

class AppWrapper extends StatelessWidget {
  const AppWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider<SessionState>(
      create: (_) {
        final state = SessionState();
        state.loadGardens();
        return state;
      },
      child: const AppContainer(),
    );
  }
}

class AppContainer extends StatelessWidget {
  const AppContainer({
    super.key,
  });

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
      home: Scaffold(
        appBar: _appBar(context),
        body: const ModalsWrapper(
          child: App(),
        ),
      ),
    );
  }

  AppBar _appBar(BuildContext context) {
    final colour = Theme.of(context).colorScheme.onPrimary;

    return AppBar(
      toolbarHeight: 40,
      leading: HoverableIcon(
        icon: Icons.arrow_back,
        height: 20,
        onTap: () {
          context.read<SessionState>().exitGarden();
        },
        colour: colour,
        hoverColour: darker(colour, amount: 40),
        clickColour: darker(colour, amount: 80),
      ),
      title: const Text(
        "Blooming Seasons Design",
        style: TextStyle(fontFamily: "Spectral", fontSize: 15),
      ),
    );
  }
}
