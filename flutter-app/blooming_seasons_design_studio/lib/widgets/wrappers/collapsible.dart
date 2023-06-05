import 'package:flutter/material.dart';

import 'hoverable.dart';

class Collapsible extends StatefulWidget {
  final Widget header;
  final Widget child;

  const Collapsible({super.key, required this.header, required this.child});

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

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Hoverable(
          builder: (BuildContext context, bool hovered, bool clicked) {
            return Container(
              padding: const EdgeInsets.all(4),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(4),
                color: clicked
                    ? Colors.blue
                    : (hovered ? Colors.blue[300] : Colors.lightBlue[50]),
              ),
              child: Row(
                children: [
                  Icon(_collapsed ? Icons.arrow_drop_down : Icons.arrow_right),
                  widget.header,
                ],
              ),
            );
          },
          onTap: () {
            setState(() {
              _collapsed = !_collapsed;
            });
          },
        ),
        if (!_collapsed) widget.child,
      ],
    );
  }
}
