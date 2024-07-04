import argparse
import sys

from analyzer.analysis import LogAnalyzer
from analyzer.log import init_logging


def main():
    init_logging()

    arg_parser = argparse.ArgumentParser(description='Analyze log files')
    arg_parser.add_argument('input', nargs='+', type=argparse.FileType('r', encoding='utf-8'),
                            help='Path to one or more log files')
    arg_parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType('w', encoding='utf-8'),
                            default=sys.stdout, help='Path to the output file, default: stdout')
    arg_parser.add_argument('--mfip', action='store_true', help='Calculate most frequent IP')
    arg_parser.add_argument('--lfip', action='store_true', help='Calculate least frequent IP')
    arg_parser.add_argument('--eps', action='store_true', help='Calculate events per second')
    arg_parser.add_argument('--bytes', action='store_true', help='Total amount of bytes exchanged')
    args = arg_parser.parse_args()

    LogAnalyzer(input_files=args.input,
                mfip=args.mfip,
                lfip=args.lfip,
                eps=args.eps,
                bytes=args.bytes,
                output=args.output).analyze_log_files()
