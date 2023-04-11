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

class Collapsible extends StatelessWidget {
  const Collapsible({
    super.key,
    required this.child,
  });

  final Widget child;

  @override
  Widget build(BuildContext context) {
    return child;
  }
}
