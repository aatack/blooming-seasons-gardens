import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../models/modals.dart';

class ModalsWrapper extends StatelessWidget {
  final Widget child;

  const ModalsWrapper({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    // NOTE: for whatever reason, this implementation creates an annoying
    //       flickering whenever the presence of some modal changes

    return BlocProvider<ModalsState>(
      create: (_) => ModalsState(),
      child: BlocBuilder<ModalsState, List<Widget>>(
        builder: (context, state) {
          if (state.isEmpty) {
            return child;
          } else {
            return Stack(
              children: [
                child,
                GestureDetector(
                  onTap: () {
                    context.read<ModalsState>().clear();
                  },
                  child: Scaffold(
                    backgroundColor: Colors.grey[700]!.withOpacity(0.5),
                    body: Center(
                      child: GestureDetector(
                        // Do not clear modals if the modal itself is tapped
                        onTap: () {},
                        child: Container(
                          color: Colors.white,
                          child: state.last,
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            );
          }
        },
      ),
    );
  }
}
