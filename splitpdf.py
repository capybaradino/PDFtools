import argparse
import os

import PyPDF2


def split_pdf(input_pdf, output_directory, pages_per_file=1):
    pdf_reader = PyPDF2.PdfReader(input_pdf)

    total_pages = len(pdf_reader.pages)

    input_file_name = os.path.basename(input_pdf)
    file_name_without_extension, file_extension = os.path.splitext(input_file_name)

    for i in range(0, total_pages, pages_per_file):
        pdf_writer = PyPDF2.PdfWriter()

        start_page = i
        end_page = min(i + pages_per_file, total_pages)

        for page_num in range(start_page, end_page):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        # page number is three digits
        output_pdf = f"{output_directory}/{file_name_without_extension}_{i//pages_per_file + 1:03d}{file_extension}"

        with open(output_pdf, "wb") as output_file:
            pdf_writer.write(output_file)


def main():
    parser = argparse.ArgumentParser(
        description="Split a PDF file into multiple PDFs with a specified number of pages each."
    )
    parser.add_argument("input_pdf", help="Input PDF file to be split")
    parser.add_argument("output_directory", help="Output directory for the split PDFs")
    parser.add_argument(
        "--pages", type=int, default=1, help="Number of pages per split PDF"
    )

    args = parser.parse_args()

    input_pdf = args.input_pdf
    output_directory = args.output_directory

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    split_pdf(input_pdf, output_directory, args.pages)


if __name__ == "__main__":
    main()
