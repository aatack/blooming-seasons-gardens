// ignore_for_file: prefer_const_constructors

import 'package:blooming_seasons_design_studio/widgets/indicators/loading.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:http/http.dart' as http;

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
        constraints: BoxConstraints(maxWidth: 400),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            NewGarden(),
            SizedBox(height: 25),
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
                    context
                        .read<SessionState>()
                        .createAndLoadNewGarden(_newGardenName);
                  }
                : null,
            child: Text("Create"),
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
        loading: () => Align(
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
      padding: EdgeInsets.only(bottom: 5),
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
          padding: EdgeInsets.all(8),
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
                        _HoverableWidget(
                          icon: Icons.edit,
                          height: height,
                          onTap: () {
                            context
                                .read<ModalsState>()
                                .add(Text("Edited ${widget.name}"));
                          },
                        ),
                        SizedBox(width: 8),
                        _HoverableWidget(
                          icon: Icons.delete,
                          height: height,
                          onTap: () {
                            context
                                .read<ModalsState>()
                                .add(Text("Deleted ${widget.name}"));
                          },
                        ),
                        SizedBox(width: 8),
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

class _HoverableWidget extends StatefulWidget {
  const _HoverableWidget(
      {required this.icon, required this.height, required this.onTap});

  final IconData icon;
  final double height;
  final void Function() onTap;

  @override
  State<_HoverableWidget> createState() => _HoverableWidgetState();
}

class _HoverableWidgetState extends State<_HoverableWidget> {
  bool _hovered = false;
  bool _clicked = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
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
        widget.onTap();
      },
      child: MouseRegion(
        onEnter: (_) {
          setState(() {
            _hovered = true;
          });
        },
        onExit: (_) {
          setState(() {
            _hovered = false;
          });
        },
        child: Icon(
          widget.icon,
          color: (_hovered && !_clicked) ? Colors.grey[700] : Colors.white,
          size: widget.height,
        ),
      ),
    );
  }
}
