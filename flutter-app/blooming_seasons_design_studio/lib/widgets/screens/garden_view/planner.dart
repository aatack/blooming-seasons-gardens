import 'package:flutter/material.dart';

class Planner extends StatelessWidget {
  const Planner({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        print("Clicked");
      },
      child: FractionallySizedBox(
        widthFactor: 1,
        heightFactor: 1,
        child: Stack(
          children: [
            GestureDetector(
                onTap: () {
                  print("Clicked background");
                },
                child: Container(color: Colors.white)),
            Positioned(
              left: 500,
              top: 100,
              child: SizedBox(
                width: 100,
                height: 100,
                child: Container(
                  decoration:
                      BoxDecoration(shape: BoxShape.circle, color: Colors.red),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
