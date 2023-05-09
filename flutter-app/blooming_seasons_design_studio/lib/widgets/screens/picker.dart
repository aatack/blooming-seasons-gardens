// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../models/garden.dart';

class GardenPicker extends StatefulWidget {
  const GardenPicker({super.key});

  @override
  State<GardenPicker> createState() => _GardenPickerState();
}

class _GardenPickerState extends State<GardenPicker> {
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
