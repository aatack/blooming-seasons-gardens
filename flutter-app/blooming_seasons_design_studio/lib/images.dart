import 'dart:html' as html;
import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart' show Image, immutable;

Future<String?> uploadImage() async {
  final uploadInput = html.FileUploadInputElement();
  uploadInput.accept = "image/*";
  uploadInput.click();

  await uploadInput.onChange.first;

  if (uploadInput.files!.isNotEmpty) {
    final file = uploadInput.files!.first;
    final reader = html.FileReader();

    reader.readAsDataUrl(file);
    await reader.onLoad.first;

    final String encodedImage = reader.result as String;

    return encodedImage.split(",")[1];
  } else {
    return null;
  }
}

Image deserialiseImage(String image) {
  final bytes = Uint8List.fromList(base64.decode(image));
  return Image.memory(bytes);
}

@immutable
class CachedImage {
  final int id;
  final String string;
  final Image image;

  const CachedImage(this.id, this.string, this.image);

  String serialise() {
    return string;
  }

  static CachedImage deserialise(int id, String image) {
    return CachedImage(id, image, deserialiseImage(image));
  }
}
