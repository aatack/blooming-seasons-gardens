import 'package:blooming_seasons_design_studio/widgets/screens/editor.dart';
import 'package:blooming_seasons_design_studio/widgets/screens/picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../models/garden.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<GardenState, Garden?>(
      builder: (context, state) {
        if (state == null) {
          return GardenPicker();
        } else {
          return GardenEditor(garden: state);
        }
      },
    );
  }
}
