// ignore_for_file: prefer_const_constructors

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:http/http.dart' as http;

import '../../models/garden.dart';

class PickGarden extends StatelessWidget {
  const PickGarden({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        constraints: BoxConstraints(maxWidth: 400),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: const [
            NewGarden(),
            LoadGarden(),
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
  const LoadGarden({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<String>>(
        future: existingGardens(),
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            return Text(snapshot.data.toString());
          } else if (snapshot.hasError) {
            return Text("Failed to load gardens");
          } else {
            return CircularProgressIndicator();
          }
        });
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
