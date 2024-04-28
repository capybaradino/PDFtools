from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageEnhance
import sys
import tempfile
import os

def jpeg_to_pdf(jpeg_file, pdf_file, brightness=1.0, margin=0):
    img = Image.open(jpeg_file)
    enhanced_img = ImageEnhance.Brightness(img).enhance(brightness)

    with tempfile.NamedTemporaryFile(delete=False) as tmp_img:
        enhanced_img.save(tmp_img, format="JPEG")
        tmp_img_path = tmp_img.name
    
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = enhanced_img.size
    c.setPageSize((width + margin * 2, height + margin * 2))  # ページサイズを余白を考慮して設定
    c.drawImage(tmp_img_path, margin, margin, width, height)  # 余白を考慮して画像を描画
    c.showPage()
    c.save()

    os.remove(tmp_img_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_jpeg_to_pdf.py <input_file.jpg> <output_file.pdf> [brightness] [margin]")
        print("brightness: Brightness factor (default is 1.0)")
        print("margin: Margin width in points (default is 0)")
        sys.exit(1)

    jpeg_file = sys.argv[1]
    pdf_file = sys.argv[2]
    brightness = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    margin = float(sys.argv[4]) if len(sys.argv) > 4 else 0
    
    jpeg_to_pdf(jpeg_file, pdf_file, brightness, margin)
