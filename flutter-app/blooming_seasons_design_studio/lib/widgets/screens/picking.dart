import 'package:blooming_seasons_design_studio/widgets/indicators/loading.dart';
import 'package:blooming_seasons_design_studio/widgets/wrappers/hoverable.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../models/modals.dart';
import '../../models/session.dart';
import '../../models/thunk.dart';
import '../indicators/error.dart';

class PickGarden extends StatelessWidget {
  const PickGarden({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        constraints: const BoxConstraints(maxWidth: 400),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const NewGarden(),
            const SizedBox(height: 25),
            BlocSelector<SessionState, Session, Thunk<List<String>>>(
              selector: (state) => state.availableGardens,
              builder: (context, gardens) => LoadGarden(gardens: gardens),
            ),
          ],
        ),
      ),
    );
  }
}

class NewGarden extends StatefulWidget {
  const NewGarden({super.key});

  @override
  State<NewGarden> createState() => _NewGardenState();
}

class _NewGardenState extends State<NewGarden> {
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
              labelText: 'New garden',
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
          child: ElevatedButton(
            onPressed: _newGardenName.isNotEmpty
                ? () {
                    context
                        .read<SessionState>()
                        .createAndLoadNewGarden(_newGardenName);
                  }
                : null,
            child: const Text("Create"),
          ),
        )
      ],
    );
  }
}

class LoadGarden extends StatelessWidget {
  final Thunk<List<String>> gardens;

  const LoadGarden({super.key, required this.gardens});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 250,
      child: gardens.handle(
        data: (data) => SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: data.map((name) => LoadGardenItem(name: name)).toList(),
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

class LoadGardenItem extends StatefulWidget {
  final String name;

  const LoadGardenItem({super.key, required this.name});

  @override
  State<LoadGardenItem> createState() => _LoadGardenItemState();
}

class _LoadGardenItemState extends State<LoadGardenItem> {
  bool _hovered = false;
  bool _clicked = false;

  @override
  Widget build(BuildContext context) {
    // TODO: determine this dynamically from the text element
    const double height = 20;

    return Container(
      padding: const EdgeInsets.only(bottom: 5),
      child: InkWell(
        onHover: (hovered) {
          setState(() {
            _hovered = hovered;
          });
        },
        onTapDown: (_) {
          setState(() {
            _clicked = true;
          });
        },
        onTapUp: (_) {
          setState(() {
            _clicked = false;
          });
        },
        onTap: () {
          context
              .read<SessionState>()
              .loadGarden(widget.name, context.read<ModalsState>());
        },
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 20),
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(4),
            color: _clicked
                ? Colors.blue
                : (_hovered ? Colors.blue[300] : Colors.lightBlue[50]),
          ),
          child: SizedBox(
            height: height,
            child: Stack(
              children: [
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    widget.name,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                if (_hovered)
                  Align(
                    alignment: Alignment.centerRight,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        HoverableIcon(
                          icon: Icons.edit,
                          height: height,
                          onTap: () {
                            context
                                .read<ModalsState>()
                                .add(Text("Edited ${widget.name}"));
                          },
                        ),
                        const SizedBox(width: 8),
                        HoverableIcon(
                          icon: Icons.delete,
                          height: height,
                          onTap: () {
                            context
                                .read<ModalsState>()
                                .add(Text("Deleted ${widget.name}"));
                          },
                        ),
                        const SizedBox(width: 8),
                      ],
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
