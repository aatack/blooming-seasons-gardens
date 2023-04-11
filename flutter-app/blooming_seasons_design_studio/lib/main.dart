import 'package:flutter/material.dart';

void main() {
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        body: Center(
          child: MainScreen(),
        ),
      ),
    );
  }
}

class MainScreen extends StatelessWidget {
  const MainScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Planner(),
        Editor(),
      ],
    );
  }
}

class Planner extends StatelessWidget {
  const Planner({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Placeholder();
  }
}

class Editor extends StatelessWidget {
  const Editor({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return FractionallySizedBox(
      widthFactor: 0.25,
      heightFactor: 1.0,
      child: ListView(
        children: [
          Collapsible(child: Placeholder()),
          Collapsible(child: Placeholder()),
          Collapsible(child: Placeholder()),
          Collapsible(child: Placeholder()),
        ],
      ),
    );
  }
}

class Collapsible extends StatefulWidget {
  Collapsible({
    super.key,
    required this.child,
  });

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
