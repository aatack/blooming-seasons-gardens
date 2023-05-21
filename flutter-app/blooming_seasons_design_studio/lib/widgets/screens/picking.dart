// ignore_for_file: prefer_const_constructors

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:http/http.dart' as http;

import '../../models/garden.dart' show GardenState;
import '../../models/loading.dart' show Loading;
import '../loading.dart' show LoadingProvider;

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
                    context.read<GardenState>().initialise(_newGardenName);
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
  const LoadGarden({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<String>>(
      future: existingGardens(),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return SizedBox(
            height: 250,
            child: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: snapshot.data!
                    .map((name) => LoadGardenItem(name: name))
                    .toList(),
              ),
            ),
          );
        } else if (snapshot.hasError) {
          return Text("Failed to load gardens:\n\n${snapshot.stackTrace}");
        } else {
          return CircularProgressIndicator();
        }
      },
    );
  }

  Future<List<String>> existingGardens() async {
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
          context.read<Loading>().setLoading("Loading ${widget.name}...");

          // TODO: asynchronously load the garden, and remove the loading
          //       spinner when done
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
          child: Text(
            widget.name,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ),
    );
  }
}
