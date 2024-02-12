# -*- coding: utf-8 -*-

__version__ = '0.1'


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
                        help="embed svg into the output (only for xml and xhtml)")
    parser.add_argument('-p', '--processor', default="auto", choices=('auto', 'html', 'xhtml'),
                        help="type of input processing")
    parser.add_argument('-V', '--verbose', action='store_true')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    # TODO ...