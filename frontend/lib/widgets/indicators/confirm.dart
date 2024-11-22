import 'package:flutter/material.dart';

import '../inputs/button.dart';

class Confirm extends StatelessWidget {
  final String message;
  final void Function() onConfirm;
  final void Function() onCancel;

  const Confirm(
      {super.key,
      required this.message,
      required this.onConfirm,
      required this.onCancel});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(message),
          const SizedBox(height: 20),
          Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Button(onClicked: onCancel, child: const Text("Cancel")),
              const SizedBox(width: 20),
              Button(onClicked: onConfirm, child: const Text("Confirm")),
            ],
          ),
        ],
      ),
    );
  }
}
