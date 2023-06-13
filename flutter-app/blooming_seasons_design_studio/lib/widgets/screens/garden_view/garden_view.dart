import 'package:blooming_seasons_design_studio/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../models/garden/garden.dart';
import '../../../models/session.dart';
import '../../wrappers/hoverable.dart';
import 'editor.dart';
import 'planner.dart';

class GardenView extends StatelessWidget {
  final Garden garden;

  const GardenView({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    const double padding = 10;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      mainAxisSize: MainAxisSize.max,
      children: [
        // Container(
        //   color: lightColorScheme.surfaceVariant,
        //   padding: const EdgeInsets.all(padding),
        //   child: Row(
        //     crossAxisAlignment: CrossAxisAlignment.center,
        //     children: [
        //       HoverableIcon(
        //         icon: Icons.arrow_back,
        //         height: 20,
        //         onTap: () {
        //           context.read<SessionState>().exitGarden();
        //         },
        //       ),
        //       const SizedBox(width: padding),
        //       Text(
        //         garden.name,
        //         style: const TextStyle(
        //           color: Colors.white,
        //           fontSize: 16,
        //           fontWeight: FontWeight.bold,
        //         ),
        //       ),
        //     ],
        //   ),
        // ),
        Expanded(
          child: Stack(
            children: [
              const Planner(),
              Editor(garden: garden),
            ],
          ),
        ),
      ],
    );
  }
}
