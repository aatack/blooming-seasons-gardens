import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../models/garden.dart';
import '../models/modals.dart';
import 'screens/editing.dart';
import 'screens/picking.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<ModalsState, List<Widget>>(
      builder: (context, modals) => BlocBuilder<GardenState, Garden?>(
        builder: (context, garden) {
          if (garden == null) {
            return const PickGarden();
          } else {
            return EditGarden(garden: garden);
          }
        },
      ),
    );
  }
}
