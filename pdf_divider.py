import PyPDF2
import copy
import argparse

def split_pdf_page(input_file, output_file):

	pdf_reader = PyPDF2.PdfReader(input_file)
	pdf_writer = PyPDF2.PdfWriter()

	for i in range(len(pdf_reader.pages)):
	    # 同じページのオブジェクトを２つ用意
	    p1 = pdf_reader.pages[i]
	    p2 = copy.copy(p1)
	    # 原稿の左下と右上の座標を取得（用紙サイズ）
	    x0 = p1.mediabox.left
	    y0 = p1.mediabox.bottom
	    x1 = p1.mediabox.right
	    y1 = p1.mediabox.top
	    # 左右に分割して切り抜く領域の座標を計算
	    p1_lower_left = (x0, y0)
	    p1_upper_right = ((x0 + x1) / 2, y1)
	    p2_lower_left = ((x0 + x1) / 2, y0)
	    p2_upper_right = (x1, y1)
	    if abs(y1 - y0) > abs(x1 - x0):
	        # 縦長の場合は上下で分割するように変える
	        p1_upper_right = (x1, (y0 + y1) / 2)
	        p2_lower_left = (x0, (y0 + y1) / 2)
	    # 切り抜く領域（cropbox）の設定
	    p1.cropbox.lower_left = p1_lower_left
	    p1.cropbox.upper_right = p1_upper_right
	    p2.cropbox.lower_left = p2_lower_left
	    p2.cropbox.upper_right = p2_upper_right
	    # 縦長の場合は上,下の順に並び替える（不要な場合はこの２行は削除）
	    if abs(y1 - y0) > abs(x1 - x0):
	        p1, p2 = p2, p1
	    # 出力用のオブジェクトに２ページ分を追加
	    pdf_writer.add_page(p1)
	    pdf_writer.add_page(p2)

	# ファイルに出力
	with open(output_file, mode="wb") as f:
	    pdf_writer.write(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a PDF page into two separate PDF files: top and bottom.")
    parser.add_argument("input_pdf", help="Input PDF file name")
    parser.add_argument("output_pdf", help="Output PDF file name")

    args = parser.parse_args()

    split_pdf_page(args.input_pdf, args.output_pdf)