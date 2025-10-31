'''
PDF Page Extractor - Extract specific pages from a PDF file.
Usage: python3 extract_pdf.py <input_pdf> <output_pdf> -s <starting_page> -e <final_page>
'''

import argparse
import sys
from PyPDF2 import PdfReader, PdfWriter


def extract_pages(input_pdf: str, output_pdf: str, start_page: str, end_page: str):
    '''
    Extract pages from a PDF file.
    Args:
        input_pdf: Path to input PDF file
        output_pdf: Path to output PDF file
        start_page: First page to extract (1-indexed)
        end_page: Last page to extract (1-indexed, inclusive)
    '''
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        total_pages = len(reader.pages)
        print(f'Total pages in PDF: {total_pages}')

        if start_page < 1 or end_page > total_pages:
            print(f'Error: Page numbers must be between 1 and {total_pages}')
            sys.exit(1)

        if start_page > end_page:
            print('Error: Start page must be less than or equal to end page')
            sys.exit(1)

        # Extract pages (convert to 0-indexed)
        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])

        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

        pages_extracted = end_page - start_page + 1
        print(f'Successfully extracted {pages_extracted} page(s) from {input_pdf}')
        print(f'Output saved to: {output_pdf}')

    except FileNotFoundError:
        print(f'Error: File "{input_pdf}" not found')
        sys.exit(1)
    except Exception as e:
        print(f'Error: {str(e)}')
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Extract specific pages from a PDF file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
            Examples:
                python extract_pdf.py input.pdf output.pdf --start 1 --end 5
                python extract_pdf.py document.pdf extracted.pdf -s 10 -e 20  
        '''
    )

    parser.add_argument('input', help='Input PDF file path')
    parser.add_argument('output', help='Output PDF file path')
    parser.add_argument(
        '-s',
        '--start',
        type=int,
        required=True,
        help='Start page number (1-indexed)'
    )
    parser.add_argument(
        '-e',
        '--end',
        type=int,
        required=True,
        help='End page number (1-indexed, inclusive)'
    )
    args = parser.parse_args()
    extract_pages(args.input, args.output, args.start, args.end)

if __name__ == '__main__':
    main()
