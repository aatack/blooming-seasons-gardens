import 'dart:html' as html;
import 'dart:convert';
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/material.dart' as material;

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

    return CachedImage(
        null, encodedImage, await _stringToUIImage(encodedImage));
  } else {
    return null;
  }
}

material.Image _stringToMaterialImage(String image) {
  final bytes = Uint8List.fromList(base64.decode(image));
  return material.Image.memory(bytes);
}

Future<ui.Image> _stringToUIImage(String image) async {
  final codec = await ui.instantiateImageCodec(
    Uint8List.fromList(base64.decode(image)),
  );
  final frame = await codec.getNextFrame();
  return frame.image;
}

@material.immutable
class CachedImage {
  final int? id;
  final String string;
  final ui.Image image;

  const CachedImage(this.id, this.string, this.image);

  String serialise() {
    return string;
  }

  static Future<CachedImage> deserialise(int id, String image) async {
    return CachedImage(id, image, await _stringToUIImage(image));
  }
}
