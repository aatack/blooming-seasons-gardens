import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../models/modals.dart';
import '../inputs/button.dart';

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
          return Stack(
            children: [
              child,
              if (state.isNotEmpty)
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
        },
      ),
    );
  }
}

Widget wrapInModal(
  BuildContext context,
  Widget modal, {
  void Function()? onConfirm,
  void Function()? onCancel,
}) {
  return Container(
    padding: const EdgeInsets.all(8),
    width: 400,
    color: Colors.grey[100],
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        modal,
        Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            if (onCancel != null)
              Button(
                  onClicked: () {
                    context.read<ModalsState>().pop();
                  },
                  child: const Text("Cancel")),
            if (onConfirm != null) const SizedBox(width: 8),
            if (onConfirm != null)
              Button(
                  onClicked: () {
                    onConfirm();
                    context.read<ModalsState>().pop();
                  },
                  child: const Text("Confirm")),
          ],
        ),
      ],
    ),
  );
}

void closeModal(BuildContext context) {
  context.read<ModalsState>().pop();
}
