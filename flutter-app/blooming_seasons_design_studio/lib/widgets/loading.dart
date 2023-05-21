import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../models/loading.dart';

class LoadingBuilder extends StatelessWidget {
  final Widget Function(BuildContext) builder;

  const LoadingBuilder({super.key, required this.builder});

  @override
  Widget build(BuildContext context) {
    return BlocProvider<Loading>(
      create: (_) => Loading(),
      child: BlocBuilder<Loading, String?>(
        builder: (context, state) {
          if (state == null) {
            return builder(context);
          } else {
            return LoadingIndicator(message: state);
          }
        },
      ),
    );
  }
}

class LoadingIndicator extends StatelessWidget {
  final String message;

  const LoadingIndicator({super.key, required this.message});

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
