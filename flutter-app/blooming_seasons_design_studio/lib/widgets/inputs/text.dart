import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../wrappers/hoverable.dart';

class ControlledTextInput extends StatefulWidget {
  final String value;
  final void Function(String) onChange;

  const ControlledTextInput(
      {super.key, required this.value, required this.onChange});

  @override
  State<ControlledTextInput> createState() => _ControlledTextInputState();
}

class _ControlledTextInputState extends State<ControlledTextInput> {
  bool _editing = false;

  @override
  Widget build(BuildContext context) {
    late Widget content;
    if (_editing) {
      content = _GreedyTextField(
          initial: widget.value,
          onDefocus: () {
            setState(() {
              _editing = false;
            });
          });
    } else {
      content = Hoverable(
        builder: (context, hovered, clicked) => Container(
          padding: const EdgeInsets.all(4),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(2),
            color: clicked
                ? Colors.grey[400]
                : (hovered ? Colors.grey[350] : Colors.grey[300]),
          ),
          child: SizedBox(
            height: 20,
            child: Stack(
              children: [
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    widget.value,
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

    return content;
  }
}

class _GreedyTextField extends StatefulWidget {
  final String initial;
  final void Function() onDefocus;

  const _GreedyTextField(
      {super.key, required this.initial, required this.onDefocus});

  @override
  State<_GreedyTextField> createState() => _GreedyTextFieldState();
}

class _GreedyTextFieldState extends State<_GreedyTextField> {
  final FocusNode _focusNode = FocusNode();
  final FocusNode _innerFocusNode = FocusNode();
  bool _isFocused = false;

  @override
  void initState() {
    super.initState();

    _focusNode.addListener(() {
      setState(() {});
    });
    _focusNode.addListener(_handleFocusChange);

    _innerFocusNode.requestFocus();
  }

  @override
  void dispose() {
    _focusNode.removeListener(_handleFocusChange);
    _focusNode.dispose();
    _innerFocusNode.dispose();
    super.dispose();
  }

  void _handleKeyEvent(RawKeyEvent event) {
    if (event.logicalKey == LogicalKeyboardKey.escape) {
      _focusNode.unfocus();
    }
  }

  void _handleFocusChange() {
    setState(() {
      _isFocused = _focusNode.hasFocus;
      if (!_isFocused) {
        // Run your callback or perform any desired actions here
        print('Text field lost focus');
        widget.onDefocus();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return RawKeyboardListener(
      focusNode: _focusNode,
      onKey: _handleKeyEvent,
      child: SizedBox(
          height: 20,
          width: 150,
          child: TextField(
              focusNode: _innerFocusNode,
              controller: TextEditingController(text: widget.initial))),
    );
  }
}
