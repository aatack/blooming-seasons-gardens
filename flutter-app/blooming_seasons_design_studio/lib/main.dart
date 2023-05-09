// ignore_for_file: prefer_const_constructors

import 'package:blooming_seasons_design_studio/models.dart'
    show Garden, GardenState;
import 'package:flutter/material.dart';
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
          return EditGardenScreen(garden: state);
        }
      },
    );
  }
}

class EditGardenScreen extends StatelessWidget {
  final Garden garden;

  const EditGardenScreen({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    return Text(garden.name);
  }
}

class SelectGardenScreen extends StatefulWidget {
  const SelectGardenScreen({super.key});

  @override
  State<SelectGardenScreen> createState() => _SelectGardenScreenState();
}

class _SelectGardenScreenState extends State<SelectGardenScreen> {
  String _newGardenName = "";

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        constraints: BoxConstraints(maxWidth: 400),
        child: Row(
          mainAxisSize: MainAxisSize.max,
          children: [
            Container(
              constraints: BoxConstraints(maxWidth: 300),
              child: TextField(
                decoration: InputDecoration(
                  labelText: 'New garden',
                ),
                onChanged: (value) {
                  setState(() {
                    _newGardenName = value;
                  });
                },
              ),
            ),
            SizedBox(width: 10),
            Expanded(
              child: ElevatedButton(
                onPressed: _newGardenName.isNotEmpty
                    ? () {
                        context.read<GardenState>().initialise(_newGardenName);
                      }
                    : null,
                child: Text("Create"),
              ),
            )
          ],
        ),
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
