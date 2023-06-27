import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../models/inputs/validated.dart';

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
  final void Function()? onEditingStarted;
  final void Function()? onEditingFinished;

  final TextStyle textStyle;

  const ControlledTextInput({
    super.key,
    required this.value,
    required this.onChange,
    this.editing = true,
    this.onEditingStarted,
    this.onEditingFinished,
    this.textStyle = const TextStyle(
      fontSize: 16,
      fontWeight: FontWeight.normal,
      color: Colors.black,
    ),
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
      if (_inputFocusNode.hasFocus) {
        _handleEditingStarted();
      } else {
        _handleEditingFinished();
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
    if (widget.value != oldWidget.value) {
      final selection = _controller.selection.copyWith();
      _controller.text = widget.value;
      _controller.selection = _controller.isSelectionWithinTextBounds(selection)
          ? selection
          : TextSelection.fromPosition(
              TextPosition(offset: widget.value.length));
    }

    if (widget.editing && !oldWidget.editing) {
      _inputFocusNode.requestFocus();
    }

    super.didUpdateWidget(oldWidget);
  }

  @override
  Widget build(BuildContext context) {
    return widget.editing ? _inputWidget(context) : _textWidget(context);
  }

  Widget _textWidget(BuildContext context) {
    return Text(widget.value,
        maxLines: 1, overflow: TextOverflow.ellipsis, style: widget.textStyle);
  }

  Widget _inputWidget(BuildContext context) {
    return RawKeyboardListener(
      focusNode: _keyboardFocusNode,
      onKey: (event) {
        if (event.logicalKey == LogicalKeyboardKey.escape) {
          _controller.text = _originalValue!;
          _controller.selection =
              TextSelection.fromPosition(const TextPosition(offset: 0));

          _inputFocusNode.unfocus();
        }
      },
      child: IntrinsicWidth(
        child: TextField(
          focusNode: _inputFocusNode,
          controller: _controller,
          decoration: null,
          style: widget.textStyle,
          onChanged: (value) {
            widget.onChange(value, true);
          },
        ),
      ),
    );
  }

  void _handleEditingStarted() {
    setState(() {
      _originalValue = widget.value;
    });

    _controller.selection =
        TextSelection.fromPosition(TextPosition(offset: widget.value.length));

    if (widget.onEditingStarted != null) {
      widget.onEditingStarted!();
    }
  }

  void _handleEditingFinished() {
    final cancelled = _controller.text == _originalValue;

    if (_originalValue != null) {
      widget.onChange(
        cancelled ? _originalValue! : _controller.text,
        cancelled,
      );

      if (widget.onEditingFinished != null) {
        widget.onEditingFinished!();
      }
    }
  }
}

Widget
    validatedTextInput<DataType, OwnType extends Validated<DataType, OwnType>>(
  Validated<DataType, OwnType> value,
  void Function(OwnType, bool) setValue,
) {
  final content = Container(
    color: value.errors.isEmpty ? Colors.white : Colors.red[100],
    child: Padding(
      padding: const EdgeInsets.only(left: 5, right: 3),
      child: ControlledTextInput(
        value: value.string,
        onChange: (newString, transient) {
          setValue(value.set(newString), transient);
        },
      ),
    ),
  );

  return Row(
    children: [
      content,
      Visibility(
        visible: value.errors.isNotEmpty,
        maintainSize: true,
        maintainAnimation: true,
        maintainState: true,
        /* For some reason, simply using a tooltip here causes the
          tooltip to grab focus every time the message goes from empty
          to non-empty.  This solution doesn't grab focus, and hence
          doesn't interfere with the text input. */
        child: Padding(
          padding: const EdgeInsets.only(left: 5),
          child: Tooltip(
            message: value.errors.join("\n"),
            child: const Icon(Icons.error_outline),
          ),
        ),
      )
    ],
  );
}
