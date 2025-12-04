#!/usr/bin/env python3
"""
Extract text from PDF file
"""
import sys

try:
    import PyPDF2
    def extract_text(pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
except ImportError:
    try:
        import pypdf
        def extract_text(pdf_path):
            with open(pdf_path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
    except ImportError:
        print("Error: PyPDF2 or pypdf library not found")
        print("Please install it with: pip3 install PyPDF2")
        sys.exit(1)

if __name__ == "__main__":
    pdf_path = "Front-Line-PHP-Book.pdf"
    try:
        text = extract_text(pdf_path)
        print(text)
    except Exception as e:
        print(f"Error extracting PDF: {e}", file=sys.stderr)
        sys.exit(1)

