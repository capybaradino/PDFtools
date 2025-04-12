import argparse
import fitz  # PyMuPDF
import os

PAGE_SIZES = {
    "A4": (595.28, 841.89),
    "LETTER": (612.0, 792.0),
    "A4_LANDSCAPE": (841.89, 595.28),
    "LETTER_LANDSCAPE": (792.0, 612.0),
    "B5": (516.0, 729.0),
    "B5_LANDSCAPE": (729.0, 516.0),
}

def get_page_size(size_name):
    size = PAGE_SIZES.get(size_name.upper())
    if not size:
        print(f"Unsupported size: {size_name}")
        print(f"Supported sizes: {', '.join(PAGE_SIZES.keys())}")
        exit(1)
    return size

def resize_pdf(input_pdf, size_name):
    width, height = get_page_size(size_name)
    output_pdf = os.path.splitext(input_pdf)[0] + f"_{size_name.upper()}.pdf"

    doc = fitz.open(input_pdf)
    new_doc = fitz.open()

    for page in doc:
        src_rect = page.rect
        scale_x = width / src_rect.width
        scale_y = height / src_rect.height
        scale = min(scale_x, scale_y)

        # 中心に配置するためのオフセット
        tx = (width - src_rect.width * scale) / 2
        ty = (height - src_rect.height * scale) / 2

        # 新しいページを作って、元ページを描画（PDFとして）
        new_page = new_doc.new_page(width=width, height=height)

        # スケーリングとオフセットを1つの行列にまとめる
        translate_matrix = fitz.Matrix(1, 0, 0, 1, tx, ty)
        scale_matrix = fitz.Matrix(scale, scale)
        matrix = scale_matrix * translate_matrix

        # 新しいページを作成し、元ページをベクターで描画
        new_page = new_doc.new_page(width=width, height=height)
        new_page.show_pdf_page(
            fitz.Rect(0, 0, width, height),
            doc,
            page.number,
            0,        # rotate
            False,    # overlay
            0,        # oc
            matrix    # transform
        )

    # 空白1ページ目の削除
    new_doc.delete_page(0)

    new_doc.save(output_pdf)
    print(f"High-quality resized PDF saved: {output_pdf}")

def main():
    parser = argparse.ArgumentParser(
        description="Resize a PDF and its content to a new page size, preserving vector quality.",
        epilog="Example: python resizePDF.py input.pdf A4"
    )
    parser.add_argument("input_pdf", help="Input PDF file name")
    parser.add_argument("size", nargs="?", default="A4", help="Target page size (default: A4)")

    args = parser.parse_args()
    resize_pdf(args.input_pdf, args.size)

if __name__ == "__main__":
    main()
