# PDFの左上端から指定サイズ部分を切り出して新しいPDFを作成する
# 入力するPDFと出力するPDFのファイル名はコマンドライン引数で指定する
# トリミングするサイズもコマンドライン引数で指定する(デフォルトはA4)
# 例: python trimB4fromA4.py input.pdf A4

import sys

from PyPDF2 import PdfReader, PdfWriter


def trimpdf(inputFile, outputFile, size):
    reader = PdfReader(inputFile)
    writer = PdfWriter()
    if size == "B4":
        xlen = 738
        ylen = 1030
    else:
        xlen = 595
        ylen = 842

    for page in reader.pages:
        # 原稿の左下と右上の座標を取得（用紙サイズ）
        # x0 = page.mediabox.left
        # y0 = page.mediabox.bottom
        # x1 = page.mediabox.right
        y1: float = page.mediabox.top
        # Update the page size to B4
        page.mediabox.lower_left = (0, y1 - ylen)
        page.mediabox.upper_right = (xlen, y1)
        writer.add_page(page)
    with open(outputFile, "wb") as out:
        writer.write(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python trimPDF.py input.pdf [A4/B4]")
        sys.exit()
    inputFile = sys.argv[1]
    outputFile = inputFile.replace(".pdf", "_trim.pdf")
    if len(sys.argv) > 2:
        size = sys.argv[2]
    else:
        size = "A4"

    trimpdf(inputFile, outputFile, size)

# 以上
