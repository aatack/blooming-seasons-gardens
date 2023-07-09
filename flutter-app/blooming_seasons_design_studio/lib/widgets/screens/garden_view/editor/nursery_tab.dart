import 'package:blooming_seasons_design_studio/models/garden/garden.dart';
import 'package:blooming_seasons_design_studio/models/modals.dart';
import 'package:blooming_seasons_design_studio/widgets/wrappers/modals.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../../models/garden/bed.dart';
import '../../../../models/garden/instance.dart';
import '../../../../models/session.dart';
import '../../../inputs/button.dart';
import '../../../inputs/elements/bed.dart';
import '../../../inputs/elements/instance.dart';

class NurseryTab extends StatelessWidget {
  final Bed nursery;

  const NurseryTab({super.key, required this.nursery});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: FractionallySizedBox(
        heightFactor: 1.0,
        child: Card(
          shape: const RoundedRectangleBorder(borderRadius: BorderRadius.zero),
          color: Colors.grey[100],
          elevation: 0,
          margin: const EdgeInsets.all(0),
          child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: ListView(
              children: [
                ...nursery.instances.map((instance) => InstanceEditor(
                      key: Key(instance.id.toString()),
                      instance: instance,
                      hidePosition: true,
                    )),
                Button(
                    onClicked: () {
                      context
                          .read<ModalsState>()
                          .add(AddElementModal(bed: nursery));
                    },
                    child: const Text("Add template")),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class NurseryModal extends StatelessWidget {
  final Garden garden;
  final int bed;

  const NurseryModal({super.key, required this.garden, required this.bed});

  @override
  Widget build(BuildContext context) {
    return wrapInModal(
      context,
      Padding(
        padding: const EdgeInsets.only(bottom: 8.0),
        child: SizedBox(
          height: 250,
          child: SingleChildScrollView(
            child: Column(
              children: [
                ...garden.nursery.instances.map(
                  (instance) => InstanceSelector(
                    key: Key(instance.id.toString()),
                    instance: instance,
                    onClick: () {
                      context.read<SessionState>().editGarden((garden) =>
                          garden.addInstance(bed,
                              element: instance.element,
                              templateID: instance.id,
                              name: instance.name));
                      context.read<ModalsState>().clear();
                    },
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
      onCancel: () {
        context.read<ModalsState>().pop();
      },
    );
  }
}
