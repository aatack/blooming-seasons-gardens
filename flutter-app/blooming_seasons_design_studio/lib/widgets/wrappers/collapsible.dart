import 'package:flutter/material.dart';

class Collapsible extends StatefulWidget {
  const Collapsible({super.key, required this.child});

  final Widget child;

  @override
  State<Collapsible> createState() => _CollapsibleState();
}

class _CollapsibleState extends State<Collapsible> {
  bool _collapsed = false;

  @override
  Widget build(BuildContext context) {
    List<Widget> children = [
      ElevatedButton(
        onPressed: () {
          setState(() {
            _collapsed = !_collapsed;
          });
        },
        child: const Text("Expand"),
      )
    ];

    if (!_collapsed) {
      children.add(widget.child);
    }

    return Column(mainAxisSize: MainAxisSize.min, children: children);
  }
}
