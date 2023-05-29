import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

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
    return Column(
      children: [
        Text(message),
        Row(
          children: [
            ElevatedButton(onPressed: onCancel, child: const Text("Cancel")),
            ElevatedButton(onPressed: onConfirm, child: const Text("Confirm")),
          ],
        ),
      ],
    );
  }
}
