import os
import sys

import PyPDF2


def combine_pdfs(pdf_files, output_filename):
    # Create a new PDF file object
    output_pdf = PyPDF2.PdfWriter()

    # Iterate over the PDF files
    for pdf_file in pdf_files:
        # Open the PDF file in read-binary mode
        with open(pdf_file, 'rb') as file:
            # Create a PDF reader object for the current file
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Iterate over each page in the PDF and add it to the new PDF file object
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                output_pdf.add_page(page)

    # Save the new PDF file with the desired name
    with open(output_filename, 'wb') as output_file:
        output_pdf.write(output_file)

# Check if the script is called with the correct arguments
if len(sys.argv) < 3:
    print("Usage: python concatpdf.py <output_filename> <pdf_file1> <pdf_file2> ...")
    sys.exit(1)

# Get the output filename and the list of PDF files from the command-line arguments
output_filename = sys.argv[1]
pdf_files = sys.argv[2:]
# outputファイルがすでに存在する場合はエラーを出力して終了
if os.path.exists(output_filename):
    print("Error: The output file %s already exists" % (output_filename))
    sys.exit(2)

# Call the function to combine the PDFs
combine_pdfs(pdf_files, output_filename)
