import 'dart:html' as html;
import 'dart:convert';
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/material.dart' show Image, immutable;

Future<CachedImage?> uploadImage() async {
  final uploadInput = html.FileUploadInputElement();
  uploadInput.accept = "image/*";
  uploadInput.click();

  await uploadInput.onChange.first;

  if (uploadInput.files!.isNotEmpty) {
    final file = uploadInput.files!.first;
    final reader = html.FileReader();

    reader.readAsDataUrl(file);
    await reader.onLoad.first;

    final String encodedImage = (reader.result as String).split(",")[1];

    return CachedImage(null, encodedImage, _stringToWidgetImage(encodedImage));
  } else {
    return null;
  }
}

Image _stringToWidgetImage(String image) {
  final bytes = Uint8List.fromList(base64.decode(image));
  return Image.memory(bytes);
}

Future<ui.Image> stringToUIImage(String image) async {
  final codec = await ui.instantiateImageCodec(
    Uint8List.fromList(base64.decode(image)),
  );
  final frame = await codec.getNextFrame();
  return frame.image;
}

@immutable
class CachedImage {
  final int? id;
  final String string;
  final Image image;

  const CachedImage(this.id, this.string, this.image);

  String serialise() {
    return string;
  }

  static CachedImage deserialise(int id, String image) {
    return CachedImage(id, image, _stringToWidgetImage(image));
  }
}
