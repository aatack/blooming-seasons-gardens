import 'package:blooming_seasons_design_studio/models/session.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

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

  late final TextEditingController _controller;

  @override
  void initState() {
    super.initState();

    _controller = TextEditingController(text: widget.value);

    // _focusNode.addListener(() {
    //   setState(() {});
    // });
    _keyboardFocusNode.addListener(_handleFocusChange);
  }

  @override
  void dispose() {
    _keyboardFocusNode.removeListener(_handleFocusChange);

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
        startEditing();
      },
    );
  }

  Widget _inputWidget(BuildContext context) {
    return RawKeyboardListener(
      focusNode: _keyboardFocusNode,
      onKey: _handleKeyEvent,
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

  void startEditing() {
    setState(() {
      _originalValue = widget.value;
    });

    _controller.text = widget.value;
    _controller.selection =
        TextSelection.fromPosition(TextPosition(offset: widget.value.length));

    _inputFocusNode.requestFocus();
  }

  // void stopEditing({bool cancelled = false}) {
  //   setState()
  // }

  void _handleFocusChange() {
    if (!_keyboardFocusNode.hasFocus && (_originalValue != null)) {
      widget.onChange(_controller.text, _controller.text == _originalValue);
      setState(() {
        _originalValue = null;
      });
    }
  }

  void _handleKeyEvent(RawKeyEvent event) {
    if ((event.logicalKey == LogicalKeyboardKey.escape) &&
        (_originalValue != null)) {
      _controller.text = _originalValue!;
      _keyboardFocusNode.unfocus();
    }
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
