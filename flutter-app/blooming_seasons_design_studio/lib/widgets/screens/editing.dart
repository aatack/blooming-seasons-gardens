import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../models/garden/garden.dart';
import '../../models/session.dart';

class EditGarden extends StatelessWidget {
  final Garden garden;

  const EditGarden({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ElevatedButton(
          onPressed: () {
            context.read<SessionState>().exitGarden();
          },
          child: const Text("Back"),
        ),
        Text(garden.name),
      ],
    );
  }
}
