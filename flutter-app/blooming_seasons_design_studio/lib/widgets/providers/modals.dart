import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../models/modals.dart';

class ModalsProvider extends StatelessWidget {
  final Widget child;

  const ModalsProvider({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
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
                Scaffold(
                  backgroundColor: Colors.grey[700]!.withOpacity(0.5),
                  body: Center(
                    child: Container(
                      color: Colors.white,
                      child: state.last,
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
