// ignore_for_file: prefer_const_constructors

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
    return FutureBuilder<String>(
        future: test(),
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            return Text(snapshot.toString());
          } else if (snapshot.hasError) {
            // return Text("Failed to load gardens");
            return Text(snapshot.toString());
          } else {
            return CircularProgressIndicator();
          }
        });
  }

  Future<String> test() async {
    final uri = Uri.parse("http://0.0.0.0:3000");
    // final uri = Uri.http("localhost:3000", "/inspect");
    final response = await http.get(uri, headers: {
      "Access-Control-Allow-Origin": "*",
      'Content-Type': 'application/json',
      'Accept': '*/*'
    });
    return response.body;
  }
}
