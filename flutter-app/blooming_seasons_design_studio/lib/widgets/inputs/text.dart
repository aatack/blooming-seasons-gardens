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
/// or not the change is transient: when the element loses focus or when
/// the user presses enter.  If the user presses escape while editing this
/// element, the callback will be fired one more time with the *original*
/// string, and with the transient flag set to `true`, indicating that the
/// user has cancelled or abandoned their changes.
///
/// To enable this to work, the widget ensures that it is only being edited
/// when it has focus.  By this mechanism, multiple of these widgets can
/// co-exist, while simultaneously guaranteeing that only one of them will
/// be being edited (and hence technically actually controlling the state)
/// at once.
class ControlledTextInput extends StatefulWidget {
  final String value;
  final void Function(String, bool) onChange;

  const ControlledTextInput(
      {super.key, required this.value, required this.onChange});

  @override
  State<ControlledTextInput> createState() => _ControlledTextInputState();
}

class _ControlledTextInputState extends State<ControlledTextInput> {
  String? _originalValue; // Defined iff the widget is being edited

  final FocusNode _keyboardFocusNode = FocusNode();
  final FocusNode _inputFocusNode = FocusNode();

  final TextEditingController _controller = TextEditingController(text: "");

  @override
  void initState() {
    super.initState();

    _keyboardFocusNode.addListener(() {
      if (!_keyboardFocusNode.hasFocus) {
        _stopEditing(cancelled: false);
      }
    });
  }

  @override
  void dispose() {
    _keyboardFocusNode.dispose();
    _inputFocusNode.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    late final Widget content;
    if (_originalValue != null) {
      content = _inputWidget(context);
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
        _startEditing();
      },
    );
  }

  Widget _inputWidget(BuildContext context) {
    return RawKeyboardListener(
      focusNode: _keyboardFocusNode,
      onKey: (event) {
        if (event.logicalKey == LogicalKeyboardKey.escape) {
          _stopEditing(cancelled: true);
        }
      },
      child: Align(
        alignment: Alignment.centerLeft,
        child: IntrinsicWidth(
          child: TextField(
            focusNode: _inputFocusNode,
            controller: _controller,
            textAlignVertical: TextAlignVertical.center,
            decoration: null,
            style: style,
            onChanged: (value) {
              widget.onChange(value, true);
            },
          ),
        ),
      ),
    );
  }

  void _startEditing() {
    setState(() {
      _originalValue = widget.value;
    });

    _controller.text = widget.value;
    _controller.selection =
        TextSelection.fromPosition(TextPosition(offset: widget.value.length));

    _inputFocusNode.requestFocus();
  }

  void _stopEditing({required bool cancelled}) {
    widget.onChange(cancelled ? _originalValue! : _controller.text, cancelled);
    setState(() {
      _originalValue = null;
    });
  }
}

const style = TextStyle(
  fontSize: 16,
  fontWeight: FontWeight.normal,
  color: Colors.black,
);
