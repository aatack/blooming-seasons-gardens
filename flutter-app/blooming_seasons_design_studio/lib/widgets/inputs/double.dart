import 'package:flutter/material.dart';

import '../../models/inputs/validated.dart';
import '../wrappers/hoverable.dart';

class DoubleInput extends StatefulWidget {
  final ValidatedDouble value;
  final void Function(ValidatedDouble) onChange;

  const DoubleInput({super.key, required this.value, required this.onChange});

  @override
  State<DoubleInput> createState() => _DoubleInputState();
}

class _DoubleInputState extends State<DoubleInput> {
  bool _editing = false;

  @override
  Widget build(BuildContext context) {
    if (_editing) {
      return greedyTextField(widget.value.string);
    } else {
      return Hoverable(
        builder: (context, hovered, clicked) => Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(4),
            color: clicked
                ? Colors.blue
                : (hovered ? Colors.blue[300] : Colors.lightBlue[50]),
          ),
          child: SizedBox(
            height: 20,
            child: Stack(
              children: const [
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    "Hello world",
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                // if (hovered) _overlayedIcons(context),
              ],
            ),
          ),
        ),
        onTap: () {
          setState(() {
            _editing = true;
          });
        },
      );
    }
  }
}

Widget greedyTextField(String initial) {
  return SizedBox(
      height: 20,
      width: 150,
      child: TextField(controller: TextEditingController(text: initial)));
}
