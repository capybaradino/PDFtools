import sys
import os
import pyheif
from PIL import Image

def convert_heic_to_jpeg(input_heic_files):
    for input_heic_file in input_heic_files:
        try:
            # JPEG ファイルのパスを生成
            output_jpeg_file = input_heic_file.replace(".HEIC", ".jpeg")

            # HEIC ファイルを開く
            heif_file = pyheif.read(input_heic_file)
            image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode, heif_file.stride)

            # JPEG ファイルに変換して保存
            image.save(output_jpeg_file, "JPEG")
            print(f"Converted {input_heic_file} to {output_jpeg_file}")
        except Exception as e:
            print(f"Error converting {input_heic_file} to JPEG: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_heic_to_jpeg.py <input_heic_file1> <input_heic_file2> ...")
        sys.exit(1)

    input_heic_files = sys.argv[1:]

    convert_heic_to_jpeg(input_heic_files)
