import 'package:blooming_seasons_gardens/theme.dart';
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

  final double actionSize = 25;
  final double actionPadding = 12;

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
      title: "Blooming Seasons Gardens",
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
    final hoverColour = darker(colour, amount: 40);
    final clickColour = darker(colour, amount: 80);

    return AppBar(
      toolbarHeight: 40,
      leading: BlocBuilder<SessionState, Session>(builder: (context, session) {
        return session.garden.handle(
          data: (_) => HoverableIcon(
            icon: Icons.arrow_back,
            height: 20,
            onTap: () {
              context.read<SessionState>().exitGarden();
            },
            colour: colour,
            hoverColour: hoverColour,
            clickColour: clickColour,
          ),
          error: (_) => Row(),
          loading: () => Row(),
        );
      }),
      title: const Text(
        "Blooming Seasons Gardens",
        style: TextStyle(fontFamily: "Spectral", fontSize: 15),
      ),
      actions: [
        BlocBuilder<SessionState, Session>(builder: (context, session) {
          return session.garden.handle(
            data: (_) => Row(
              children: [
                _appBarAction(
                  context,
                  icon: Icons.undo,
                  onTap: (session.garden
                              .fmap((history) => history.canGoBack)
                              .unpack() ??
                          false)
                      ? () {
                          context.read<SessionState>().undo();
                        }
                      : null,
                  colour: colour,
                  hoverColour: hoverColour,
                  clickColour: clickColour,
                ),
                _appBarAction(
                  context,
                  icon: Icons.redo,
                  onTap: (session.garden
                              .fmap((history) => history.canGoForward)
                              .unpack() ??
                          false)
                      ? () {
                          context.read<SessionState>().redo();
                        }
                      : null,
                  colour: colour,
                  hoverColour: hoverColour,
                  clickColour: clickColour,
                ),
                _appBarAction(
                  context,
                  icon: Icons.save,
                  onTap: () {
                    context.read<SessionState>().saveGarden();
                  },
                  colour: colour,
                  hoverColour: hoverColour,
                  clickColour: clickColour,
                ),
              ],
            ),
            error: (_) => Row(),
            loading: () => Row(),
          );
        }),
      ],
    );
  }

  Widget _appBarAction(
    BuildContext context, {
    required IconData icon,
    required void Function()? onTap,
    required Color colour,
    required Color hoverColour,
    required Color clickColour,
  }) {
    return Padding(
      padding: EdgeInsets.only(right: actionPadding),
      child: HoverableIcon(
        icon: icon,
        height: actionSize,
        onTap: onTap,
        colour: colour,
        hoverColour: hoverColour,
        clickColour: clickColour,
      ),
    );
  }
}
