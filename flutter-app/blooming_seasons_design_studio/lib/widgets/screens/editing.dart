import 'package:blooming_seasons_design_studio/widgets/wrappers/hoverable.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../models/garden/garden.dart';
import '../../models/session.dart';

class EditGarden extends StatelessWidget {
  final Garden garden;

  const EditGarden({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    const double padding = 10;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      mainAxisSize: MainAxisSize.max,
      children: [
        Container(
          color: Colors.blue[800],
          padding: const EdgeInsets.all(padding),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              HoverableIcon(
                icon: Icons.arrow_back,
                height: 20,
                onTap: () {
                  context.read<SessionState>().exitGarden();
                },
              ),
              const SizedBox(width: padding),
              Text(garden.name,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  )),
            ],
          ),
        ),
        Expanded(child: const Placeholder()),
      ],
    );
  }
}
