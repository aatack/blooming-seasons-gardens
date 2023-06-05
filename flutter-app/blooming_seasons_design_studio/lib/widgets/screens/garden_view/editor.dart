import 'package:flutter/material.dart';

import '../../../models/garden/garden.dart';
import '../../wrappers/collapsible.dart';
import '../../wrappers/resizable.dart';

class Editor extends StatelessWidget {
  final Garden garden;

  const Editor({super.key, required this.garden});

  @override
  Widget build(BuildContext context) {
    return FractionallySizedBox(
      child: Resizable(
        initialWidth: 200,
        child: Container(
          color: Colors.white,
          child: Column(
              // children: garden.beds.map((bed) => BedWidget(bed: bed)).toList(),
              children: const [
                HeaderButtons(),
                Collapsible(header: Text("Header"), child: Text("Child"))
              ]),
        ),
      ),
    );
  }
}

class HeaderButtons extends StatelessWidget {
  const HeaderButtons({super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        ElevatedButton(
          onPressed: () {},
          child: const Text(
            "New bed",
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
        ElevatedButton(
          onPressed: () {},
          child: const Text(
            "Templates",
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ].map((element) => wrap(element)).toList(),
    );
  }

  Widget wrap(Widget widget) {
    return Expanded(
      child: Container(
        // TODO: shrink the ugly space between the buttons
        padding: const EdgeInsets.all(4),
        child: widget,
      ),
    );
  }
}
