import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../models/modals.dart';

class ModalsProvider extends StatelessWidget {
  final Widget child;

  const ModalsProvider({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return BlocProvider<ModalsState>(
      create: (_) => ModalsState(),
      child: child,
    );
  }
}
