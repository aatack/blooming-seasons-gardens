import 'package:blooming_seasons_design_studio/widgets/indicators/error.dart';
import 'package:blooming_seasons_design_studio/widgets/indicators/loading.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../models/session.dart';
import 'screens/picking.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<SessionState, Session>(
      builder: (context, session) {
        if (session.currentGarden.isEmpty) {
          return const PickGarden();
        } else {
          return session.currentGarden.handle(
            data: (data) => Text(data.name),
            error: (error) => ErrorIndicator(message: error.toString()),
            loading: () => const Center(
              child: LoadingIndicator(message: "Loading garden"),
            ),
            empty: () => const PickGarden(),
          );
        }
      },
    );
  }
}
