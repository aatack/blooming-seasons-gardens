import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../models/modals.dart';
import '../../models/session.dart';
import '../../models/thunk.dart';
import '../../theme.dart';
import '../indicators/error.dart';
import '../indicators/loading.dart';
import '../inputs/button.dart';
import '../wrappers/hoverable.dart';

class LandingPage extends StatelessWidget {
  const LandingPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        constraints: const BoxConstraints(maxWidth: 400),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const _NewGarden(),
            const SizedBox(height: 25),
            BlocSelector<SessionState, Session, Thunk<List<String>>>(
              selector: (state) => state.gardens,
              builder: (context, gardens) => _LoadGarden(gardens: gardens),
            ),
          ],
        ),
      ),
    );
  }
}

class _NewGarden extends StatefulWidget {
  const _NewGarden({super.key});

  @override
  State<_NewGarden> createState() => _NewGardenState();
}

class _NewGardenState extends State<_NewGarden> {
  String _newGardenName = "";

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.max,
      children: [
        Container(
          constraints: const BoxConstraints(maxWidth: 300),
          child: TextField(
            decoration: const InputDecoration(
              labelText: "New garden",
            ),
            onChanged: (value) {
              setState(() {
                _newGardenName = value;
              });
            },
          ),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: Button(
            onClicked: _newGardenName.isNotEmpty
                ? () {
                    context.read<SessionState>().createGarden(
                          _newGardenName,
                          context.read<ModalsState>(),
                        );
                  }
                : null,
            emphasise: true,
            child: const Text("Create"),
          ),
        )
      ],
    );
  }
}

class _LoadGarden extends StatelessWidget {
  final Thunk<List<String>> gardens;

  const _LoadGarden({required this.gardens});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 250,
      child: gardens.handle(
        data: (data) => SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: data.map((name) => _LoadGardenItem(name: name)).toList(),
          ),
        ),
        error: (error) => ErrorIndicator(message: error.toString()),
        loading: () => const Align(
          alignment: Alignment.topCenter,
          child: LoadingIndicator(message: "Loading gardens"),
        ),
      ),
    );
  }
}

class _LoadGardenItem extends StatelessWidget {
  final double height = 20;

  final String name;

  const _LoadGardenItem({super.key, required this.name});

  @override
  Widget build(BuildContext context) {
    return Hoverable(
      builder: (context, hovered, clicked) => Container(
        padding: const EdgeInsets.only(bottom: 5),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 20),
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(4),
            color: clicked
                ? AppTheme.backgroundColour
                : (hovered
                    ? AppTheme.backgroundColour[500]
                    : AppTheme.backgroundColour[200]),
          ),
          child: SizedBox(
            height: height,
            child: Stack(
              children: [
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    name,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                if (hovered) _overlayedIcons(context),
              ],
            ),
          ),
        ),
      ),
      onTap: () {
        context
            .read<SessionState>()
            .loadGarden(name, context.read<ModalsState>());
      },
    );
  }

  Widget _overlayedIcons(BuildContext context) {
    return Align(
      alignment: Alignment.centerRight,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          HoverableIcon(
            icon: Icons.edit,
            height: height,
            onTap: () {
              final modals = context.read<ModalsState>();

              modals.add(_RenameGarden(name));
            },
          ),
          const SizedBox(width: 8),
          HoverableIcon(
            icon: Icons.delete,
            height: height,
            onTap: () {
              context.read<ModalsState>().confirm(
                    message: "Delete garden $name?",
                    action: () {
                      context.read<SessionState>().deleteGarden(
                            name,
                            context.read<ModalsState>(),
                          );
                    },
                  );
            },
          ),
          const SizedBox(width: 8),
        ],
      ),
    );
  }
}

class _RenameGarden extends StatefulWidget {
  final String oldName;

  const _RenameGarden(this.oldName);

  @override
  State<_RenameGarden> createState() => _RenameGardenState();
}

class _RenameGardenState extends State<_RenameGarden> {
  String _newName = "";

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            constraints: const BoxConstraints(maxWidth: 400),
            child: TextField(
              decoration: const InputDecoration(
                labelText: "New garden name",
              ),
              onChanged: (value) {
                setState(() {
                  _newName = value;
                });
              },
            ),
          ),
          const SizedBox(height: 20),
          Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Button(
                onClicked: () {
                  context.read<ModalsState>().pop();
                },
                child: const Text("Cancel"),
              ),
              const SizedBox(width: 20),
              Button(
                onClicked: (_newName.isNotEmpty && (_newName != widget.oldName))
                    ? () {
                        final modals = context.read<ModalsState>();

                        modals.pop();
                        context.read<SessionState>().renameGarden(
                              widget.oldName,
                              _newName,
                              modals,
                            );
                      }
                    : null,
                child: const Text("Confirm"),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
