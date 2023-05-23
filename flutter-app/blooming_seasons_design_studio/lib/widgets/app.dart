import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../models/garden.dart';
import '../models/session.dart';
import 'screens/editing.dart';
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
          return EditGarden(garden: Garden.blank("Placeholder"));
        }
      },
    );
  }
}
