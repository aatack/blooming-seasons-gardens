import 'dart:html' as html;
import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart' show Image;

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
