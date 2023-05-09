import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'models/garden.dart' show GardenState;
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
      home: BlocProvider<GardenState>(
        create: (_) => GardenState(),
        child: const Scaffold(
          body: App(),
        ),
      ),
    );
  }
}
