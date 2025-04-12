# 指定したファイルの指定したページを90度時計回りに回転させる
# 使い方: python3 rotate.py <ファイル名> <ページ番号>
# 例: python3 rotate.py sample.pdf 1
# ページ番号を省略した場合は、すべてのページを回転させる

import sys

from PyPDF2 import PdfReader, PdfWriter


def rotate_pdf(input_file, output_file, page_num):
    pdf_reader = PdfReader(input_file)
    pdf_writer = PdfWriter()

    for page in range(len(pdf_reader.pages)):
        if page_num is None or page + 1 in page_num:
            pdf_writer.add_page(pdf_reader.pages[page].rotate(90))
        else:
            pdf_writer.add_page(pdf_reader.pages[page])

    with open(output_file, "wb") as f:
        pdf_writer.write(f)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 rotate.py <input_file> [page_num]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file.replace(".pdf", "_rotated.pdf")
    page_num = None

    if len(sys.argv) == 3:
        page_num = [int(sys.argv[2])]

    rotate_pdf(input_file, output_file, page_num)
    print("PDF rotated successfully. file : ", output_file)
