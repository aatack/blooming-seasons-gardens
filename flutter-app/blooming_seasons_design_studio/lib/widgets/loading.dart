import 'package:flutter/material.dart';

class LoadingMessage extends StatelessWidget {
  final String message;

  const LoadingMessage({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const CircularProgressIndicator(),
          const SizedBox(height: 25),
          Text(message),
        ],
      ),
    );
  }
}
