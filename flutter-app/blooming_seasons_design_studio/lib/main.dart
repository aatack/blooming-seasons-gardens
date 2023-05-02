// ignore_for_file: prefer_const_constructors

import 'package:blooming_seasons_design_studio/models.dart'
    show Garden, GardenState;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

void main() {
  runApp(const AppWrapper());
}

class AppWrapper extends StatelessWidget {
  const AppWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Blooming Seasons Design Studio",
      home: BlocProvider<GardenState>(
        create: (_) => GardenState(),
        child: Scaffold(
          body: App(),
        ),
      ),
    );
  }
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<GardenState, Garden?>(
      builder: (context, state) {
        if (state == null) {
          return SelectGardenScreen();
        } else {
          return Text(state.name);
        }
      },
    );
  }
}

class SelectGardenScreen extends StatefulWidget {
  const SelectGardenScreen({super.key});

  @override
  State<SelectGardenScreen> createState() => _SelectGardenScreenState();
}

class _SelectGardenScreenState extends State<SelectGardenScreen> {
  final _textController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          TextField(
            controller: _textController,
            decoration: InputDecoration(
              labelText: 'Create new garden',
            ),
          ),
          ElevatedButton(
            onPressed: () {
              context.read<GardenState>().initialise(_textController.text);
            },
            child: Text("Create"),
          )
        ],
      ),
    );
  }
}

// class MainScreen extends StatelessWidget {
//   const MainScreen({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return Stack(
//       children: [
//         Planner(),
//         Editor(),
//       ],
//     );
//   }
// }

// class Planner extends StatelessWidget {
//   const Planner({
//     super.key,
//   });

//   @override
//   Widget build(BuildContext context) {
//     return Placeholder();
//   }
// }

// class Editor extends StatelessWidget {
//   const Editor({
//     super.key,
//   });

//   @override
//   Widget build(BuildContext context) {
//     return FractionallySizedBox(
//       widthFactor: 0.25,
//       heightFactor: 1.0,
//       child: ListView(
//         children: [
//           Collapsible(child: Placeholder()),
//           Collapsible(child: Placeholder()),
//           Collapsible(child: Placeholder()),
//           Collapsible(child: Placeholder()),
//         ],
//       ),
//     );
//   }
// }

// class Collapsible extends StatefulWidget {
//   Collapsible({
//     super.key,
//     required this.child,
//   });

//   final Widget child;

//   @override
//   State<Collapsible> createState() => _CollapsibleState();
// }

// class _CollapsibleState extends State<Collapsible> {
//   bool _collapsed = false;

//   @override
//   Widget build(BuildContext context) {
//     List<Widget> children = [
//       ElevatedButton(
//         onPressed: () {
//           setState(() {
//             _collapsed = !_collapsed;
//           });
//         },
//         child: const Text("Expand"),
//       )
//     ];

//     if (!_collapsed) {
//       children.add(widget.child);
//     }

//     return Column(mainAxisSize: MainAxisSize.min, children: children);
//   }
// }
