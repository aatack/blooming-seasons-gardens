import 'package:blooming_seasons_design_studio/widgets/modals.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../models/garden.dart';
import 'screens/editing.dart';
import 'screens/picking.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return ModalsProvider(
      child: BlocBuilder<GardenState, Garden?>(
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
