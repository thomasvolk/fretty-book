# -*- coding: utf-8 -*-
from .processor import HTMLDocumentProcessor, XHTMLDocumentProcessor, MarkdownDocumentProcessor, OrgDocumentProcessor

__version__ = '0.3'


def _auto_detect(input_file):
    f = input_file.lower()
    if f.endswith('.xhtml'):
        return XHTMLDocumentProcessor
    if f.endswith(('.html', '.htm')):
        return HTMLDocumentProcessor
    if f.endswith('.org'):
        return OrgDocumentProcessor
    return MarkdownDocumentProcessor


_processors = {
    'html':     lambda _f: HTMLDocumentProcessor,
    'xhtml':    lambda _f: XHTMLDocumentProcessor,
    'markdown': lambda _f: MarkdownDocumentProcessor,
    'org':      lambda _f: OrgDocumentProcessor,
    'auto':     _auto_detect,
}


def main():
    import argparse

    parser = argparse.ArgumentParser(
                prog='fretty-book',
                description='fretty-book can replace inline fretty markup within documents with the generated images'
                )
    parser.add_argument('input_file')
    parser.add_argument('-o', '--output-file', help="output file name")
    parser.add_argument('--png', action='store_true', help="use png images files instead of svg")
    parser.add_argument('-e', '--embed-svg', action='store_true',
                        help="embed svg into the document")
    parser.add_argument('-p', '--processor', default="auto", choices=list(_processors.keys()),
                        help=f"type of input processing {list(_processors.keys())} (auto tryes to determine the processor by the file extension)")
    parser.add_argument('-V', '--verbose', action='store_true')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    processor_class = _processors[args.processor](args.input_file)

    if args.embed_svg and processor_class in (MarkdownDocumentProcessor, OrgDocumentProcessor):
        parser.error("--embed-svg is not supported for markdown and org formats")

    if args.verbose:
        print(f"use processor: {processor_class.__name__}")
    
    processor = processor_class(embedded=args.embed_svg, png_images=args.png, output_file=args.output_file)
    output = processor.process_file(args.input_file)
    
    if args.output_file:
        if args.verbose:
            print(f"write file: {args.output_file}")
        with open(args.output_file, 'w') as o:
            o.write(output)
    else:
        print(output)
