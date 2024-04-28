import argparse

from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def convert_images_to_pdf(image_files, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter

    for image_file in image_files:
        img = Image.open(image_file)
        img_width, img_height = img.size

        # Calculate the aspect ratio to fit the image within the PDF page
        aspect_ratio = img_width / img_height
        new_width = width
        new_height = width / aspect_ratio

        if new_height > height:
            new_height = height
            new_width = height * aspect_ratio

        c.setPageSize((new_width, new_height))
        c.drawImage(image_file, 0, 0, width=new_width, height=new_height)
        c.showPage()

    c.save()


def main():
    parser = argparse.ArgumentParser(
        description="Convert a list of image files into a single PDF."
    )
    parser.add_argument(
        "image_files", nargs="+", help="List of image files to be converted into a PDF"
    )
    parser.add_argument("--output", default="output.pdf", help="Output PDF file name")

    args = parser.parse_args()

    image_files = args.image_files
    output_pdf = args.output

    convert_images_to_pdf(image_files, output_pdf)


if __name__ == "__main__":
    main()
