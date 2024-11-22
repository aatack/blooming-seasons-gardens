import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../models/session.dart';
import 'indicators/error.dart';
import 'indicators/loading.dart';
import 'screens/garden_view/garden_view.dart';
import 'screens/landing_page.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<SessionState, Session>(
      builder: (context, session) {
        if (session.garden.isEmpty) {
          return const LandingPage();
        } else {
          return session.garden.handle(
            data: (data) => GardenView(
                garden: data.present, selections: session.selections),
            error: (error) => ErrorIndicator(message: error.toString()),
            loading: () => const Center(
              child: LoadingIndicator(message: "Loading garden"),
            ),
            empty: () => const LandingPage(),
          );
        }
      },
    );
  }
}
