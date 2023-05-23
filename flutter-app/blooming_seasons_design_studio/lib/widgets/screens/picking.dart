// ignore_for_file: prefer_const_constructors

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:http/http.dart' as http;

import '../../models/modals.dart';
import '../../models/session.dart';
import '../providers/loading.dart';

class PickGarden extends StatelessWidget {
  const PickGarden({super.key});

  @override
  Widget build(BuildContext context) {
    return LoadingProvider(
      child: Center(
        child: Container(
          constraints: BoxConstraints(maxWidth: 400),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: const [
              NewGarden(),
              SizedBox(height: 25),
              LoadGarden(),
            ],
          ),
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

class LoadGarden extends StatefulWidget {
  // TODO: move this state into the `GardenState`, and rename it to `AppState`

  const LoadGarden({super.key});

  @override
  State<LoadGarden> createState() => _LoadGardenState();
}

class _LoadGardenState extends State<LoadGarden> {
  List<String>? _gardens;
  String? _error;

  @override
  void initState() {
    super.initState();

    if (_gardens == null) {
      _refreshGardens().then((data) {
        setState(() {
          _gardens = data;
          _error = null;
        });
      }).catchError((error) {
        setState(() {
          _gardens = null;
          _error = "Failed to load gardens: ${error.toString()}";
        });
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_gardens != null) {
      return SizedBox(
        height: 250,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children:
                _gardens!.map((name) => LoadGardenItem(name: name)).toList(),
          ),
        ),
      );
    } else {
      return Text(_error.toString());
    }
  }

  Future<List<String>> _refreshGardens() async {
    final response =
        await http.get(Uri.parse("http://localhost:3000/gardens/list"));

    if (response.statusCode == 200) {
      final jsonResponse = jsonDecode(response.body);
      if (jsonResponse is List<dynamic>) {
        return List<String>.from(jsonResponse);
      } else {
        throw FormatException(
            "Response was not formatted as a list of strings");
      }
    } else {
      throw Exception("Could not load existing gardens");
    }
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
          loadGarden(
            widget.name,
            context.read<SessionState>(),
            context.read<ModalsState>(),
          );
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

  Future<void> loadGarden(
      String name, SessionState session, ModalsState modals) async {
    final escapedName = name; // TODO: escape the name properly
    try {
      final response = await http
          .get(Uri.parse("http://localhost:3000/gardens/get/$escapedName"));

      if (response.statusCode == 200) {
        // garden.initialise(response.body);
      } else {
        modals.add(Text("Error from server: ${response.body}"));
      }
    } catch (e) {
      modals.add(Text("Error from client: $e"));
    }
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
