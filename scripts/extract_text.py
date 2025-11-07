'''
PDF Text Extractor - Extract text from PDF files with optional metadata.
Usage:
    python extract_text.py <input_pdf> <output_txt>
    python extract_text.py <input_pdf> <output_txt> --detailed
'''

import sys
import argparse
from PyPDF2 import PdfReader


def extract_text(pdf_path):
    '''Extract plain text from PDF.'''
    reader = PdfReader(pdf_path)
    text = []

    for page_num, page in enumerate(reader.pages, 1):
        text.append(f'--- Page {page_num} ---\n')
        text.append(page.extract_text())

    return ''.join(text)


def extract_detailed(pdf_path):
    '''Extract text and metadata from PDF.'''
    reader = PdfReader(pdf_path)

    metadata = reader.metadata
    info = []
    info.append('=' * 50)
    info.append('\nPDF INFORMATION\n')
    info.append('=' * 50 + '\n\n')

    if metadata:
        info.append(f'Title: {metadata.get('/Title', 'N/A')}\n')
        info.append(f'Author: {metadata.get('/Author', 'N/A')}\n')
        info.append(f'Subject: {metadata.get('/Subject', 'N/A')}\n')
        info.append(f'Creator: {metadata.get('/Creator', 'N/A')}\n')
        info.append(f'Producer: {metadata.get('/Producer', 'N/A')}\n')
        info.append(f'Creation Date: {metadata.get('/CreationDate', 'N/A')}\n')
    else:
        info.append('No metadata available\n')

    info.append(f'\nTotal Pages: {len(reader.pages)}\n')
    info.append('\n' + '=' * 50 + '\n')
    info.append('CONTENT\n')
    info.append('=' * 50 + '\n')

    for page_num, page in enumerate(reader.pages, 1):
        info.append(f'--- Page {page_num} ---\n')
        info.append(page.extract_text())

    return ''.join(info)


def main():
    parser = argparse.ArgumentParser(
        description='Extract text from PDF files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    %(prog)s input.pdf output.txt
    %(prog)s input.pdf output.txt --detailed
'''
    )

    parser.add_argument(
        'input_pdf',
        help='Input PDF file path'
    )
    parser.add_argument(
        'output_txt',
        help='Output TXT file path'
    )
    parser.add_argument(
        '-d',
        '--detailed',
        action='store_true',
        help='Include PDF metadata and additional information')

    args = parser.parse_args()

    try:
        print(f'Processing: {args.input_pdf}')

        if args.detailed:
            print('Mode: Detailed extraction (with metadata)')
            content = extract_detailed(args.input_pdf)
        else:
            print('Mode: Simple extraction (text only)')
            content = extract_text(args.input_pdf)

        with open(args.output_txt, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f'Successfully saved to: {args.output_txt}')

    except FileNotFoundError:
        print(f'Error: File "{args.input_pdf}" not found', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
