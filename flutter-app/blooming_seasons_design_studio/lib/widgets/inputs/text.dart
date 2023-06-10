import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../wrappers/hoverable.dart';

/// A controlled text input, mimicking the React style of data entry.
///
/// While the text input is not being edited, it will reactively display
/// whatever text is passed to its `value` property.  While it is being
/// edited, it will display the currently edited text.
///
/// Every time the text inside is changed, the `onChange` callback will
/// be fired with the new string.  The boolean argument represents whether
/// or not the change is a "commit": when the element loses focus or when
/// the user presses enter.  If the user presses escape while editing this
/// element, the callback will be fired one more time with the *original*
/// string, and with the commit flag set to `false`, indicating that the
/// user has cancelled or abandoned their changes.
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
    late final Widget content;
    if (_editing) {
      content = _GreedyTextField(
          initial: widget.value,
          onChange: (value, commit) {
            print("$value ($commit)");
          },
          onDefocus: () {
            setState(() {
              _editing = false;
            });
          });
    } else {
      content = Text(widget.value,
          maxLines: 1, overflow: TextOverflow.ellipsis, style: style);
    }

    return Hoverable(
      builder: (context, hovered, clicked) => Container(
        alignment: Alignment.centerLeft,
        padding: const EdgeInsets.all(4),
        decoration: BoxDecoration(
          color: clicked
              ? Colors.grey[400]
              : (hovered ? Colors.grey[350] : Colors.grey[300]),
        ),
        child: content,
      ),
      onTap: () {
        setState(() {
          _editing = true;
        });
      },
    );
  }
}

class _GreedyTextField extends StatefulWidget {
  final String initial;
  final void Function(String, bool) onChange;
  final void Function() onDefocus;

  const _GreedyTextField(
      {required this.initial, required this.onChange, required this.onDefocus});

  @override
  State<_GreedyTextField> createState() => _GreedyTextFieldState();
}

class _GreedyTextFieldState extends State<_GreedyTextField> {
  final FocusNode _focusNode = FocusNode();
  final FocusNode _innerFocusNode = FocusNode();
  late final TextEditingController _controller;

  bool _isFocused = false;

  @override
  void initState() {
    super.initState();

    _controller = TextEditingController(text: widget.initial);
    _controller.selection = TextSelection.fromPosition(
        TextPosition(offset: _controller.text.length));

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
      _controller.text = widget.initial;
      _focusNode.unfocus();
    }
  }

  void _handleFocusChange() {
    setState(() {
      _isFocused = _focusNode.hasFocus;
      if (!_isFocused) {
        widget.onDefocus();
        widget.onChange(_controller.text, _controller.text != widget.initial);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return RawKeyboardListener(
      focusNode: _focusNode,
      onKey: _handleKeyEvent,
      child: Align(
        alignment: Alignment.centerLeft,
        child: IntrinsicWidth(
          child: TextField(
            focusNode: _innerFocusNode,
            controller: _controller,
            textAlignVertical: TextAlignVertical.center,
            decoration: null,
            style: style,
            onChanged: (value) {
              widget.onChange(value, false);
            },
          ),
        ),
      ),
    );
  }
}

const style = TextStyle(
  fontSize: 16,
  fontWeight: FontWeight.normal,
  color: Colors.black,
);
