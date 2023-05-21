import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../models/loading.dart';

class LoadingWrapper extends StatelessWidget {
  final Widget child;

  const LoadingWrapper({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return BlocProvider<Loading>(
      create: (_) => Loading(),
      child: BlocBuilder<Loading, String?>(
        builder: (context, state) {
          if (state == null) {
            return child;
          } else {
            return _LoadingIndicator(message: state);
          }
        },
      ),
    );
  }
}

class _LoadingIndicator extends StatelessWidget {
  final String message;

  const _LoadingIndicator({required this.message});

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
