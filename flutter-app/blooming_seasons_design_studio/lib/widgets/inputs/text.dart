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

  final bool editing;
  final void Function() onEditingFinished;

  const ControlledTextInput({
    super.key,
    required this.value,
    required this.onChange,
    this.editing = true,
    this.onEditingFinished = _doNothing,
  });

  @override
  State<ControlledTextInput> createState() => _ControlledTextInputState();
}

class _ControlledTextInputState extends State<ControlledTextInput> {
  String? _originalValue;

  final FocusNode _keyboardFocusNode = FocusNode();
  final FocusNode _inputFocusNode = FocusNode();

  late final TextEditingController _controller;

  @override
  void initState() {
    super.initState();

    _inputFocusNode.addListener(() {
      if (!_keyboardFocusNode.hasFocus) {
        _stopEditing(cancelled: false);
      }
    });

    _controller = TextEditingController(text: widget.value);
  }

  @override
  void dispose() {
    _keyboardFocusNode.dispose();
    _inputFocusNode.dispose();

    super.dispose();
  }

  @override
  void didUpdateWidget(ControlledTextInput oldWidget) {
    final selection = _controller.selection.copyWith();
    _controller.text = widget.value;
    _controller.selection = selection;

    super.didUpdateWidget(oldWidget);
  }

  @override
  Widget build(BuildContext context) {
    late final Widget content;
    if (widget.editing) {
      content = _inputWidget(context);
    } else {
      content = Text(widget.value,
          maxLines: 1, overflow: TextOverflow.ellipsis, style: style);
    }

    return Container(
      alignment: Alignment.centerLeft,
      padding: const EdgeInsets.all(4),
      decoration: BoxDecoration(
        color: Colors.grey[300],
      ),
      child: content,
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

    _controller.selection =
        TextSelection.fromPosition(TextPosition(offset: widget.value.length));

    _inputFocusNode.requestFocus();
  }

  void _stopEditing({required bool cancelled}) {
    if (_originalValue != null) {
      // If the original value was never set, this widget is permanently being
      // edited, so cannot be reset/cancelled

      widget.onChange(
        cancelled ? _originalValue! : _controller.text,
        cancelled,
      );

      widget.onEditingFinished();
    }
  }
}

const style = TextStyle(
  fontSize: 16,
  fontWeight: FontWeight.normal,
  color: Colors.black,
);

void _doNothing() {}
