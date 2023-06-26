import 'package:flutter/material.dart';

class FormLayoutItem {
  final Widget label;
  final Widget child;

  const FormLayoutItem({required this.label, required this.child});
}

class FormLayout extends StatelessWidget {
  final List<FormLayoutItem> children;
  final double rowSpacing;
  final double columnSpacing;

  const FormLayout({
    super.key,
    required this.children,
    this.rowSpacing = 5,
    this.columnSpacing = 5,
  });

  @override
  Widget build(BuildContext context) {
    final spacer = TableRow(children: [
      SizedBox(height: rowSpacing),
      SizedBox(height: rowSpacing),
      SizedBox(height: rowSpacing)
    ]);

    return Table(
      columnWidths: const {
        0: IntrinsicColumnWidth(),
        1: IntrinsicColumnWidth(),
        2: FlexColumnWidth()
      },
      defaultVerticalAlignment: TableCellVerticalAlignment.middle,
      children: intersperse(
        children
            .map((child) => TableRow(children: [
                  child.label,
                  SizedBox(width: columnSpacing),
                  child.child,
                ]))
            .toList(),
        spacer,
      ).toList(),
    );
  }
}

List<T> intersperse<T>(List<T> items, T spacer) {
  final List<T> result = [];

  for (int index = 0; index < items.length; index++) {
    result.add(items[index]);
    if (index < items.length - 1) {
      result.add(spacer);
    }
  }

  return result;
}
