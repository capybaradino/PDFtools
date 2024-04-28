# A4サイズのPDFの左上端からB4サイズ部分を切り出して新しいPDFを作成する
# 入力するPDFと出力するPDFのファイル名はコマンドライン引数で指定する
# 例: python trimB4fromA4.py input.pdf output.pdf

import sys

from PyPDF2 import PdfReader, PdfWriter


def trimB4fromA4(inputFile, outputFile):
    reader = PdfReader(inputFile)
    writer = PdfWriter()
    for page in reader.pages:
        # 原稿の左下と右上の座標を取得（用紙サイズ）
        x0 = page.mediabox.left
        y0 = page.mediabox.bottom
        x1 = page.mediabox.right
        y1: float = page.mediabox.top
        # Update the page size to B4
        page.mediabox.lower_left = (0, y1 - 1030)
        page.mediabox.upper_right = (738, y1)
        writer.add_page(page)
    with open(outputFile, "wb") as out:
        writer.write(out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python trimB4fromA4.py input.pdf output.pdf")
        sys.exit()
    trimB4fromA4(sys.argv[1], sys.argv[2])

# 以上
