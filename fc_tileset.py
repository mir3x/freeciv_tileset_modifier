##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##
##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##
##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##
##=##=##=# You are not meant to understand this ##=##=##=##=##
##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##
##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##
##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##

import os
import errno
import sys
from argparse import ArgumentParser

def load_dir(dir_name):
    pass

def load_spec(filename):
    pass

def save_spec(filename):
    pass

def load_img(filename):
    pass

def main(input_dir, output_dir):
    pass

if __name__ == '__main__':
    parser = ArgumentParser(description='Freeciv Tileset Modifier')
    parser.add_argument('input_dir', nargs='?', default='trident',
                        help='Tileset directory (default: %(default)s)')
    parser.add_argument('-output_dir', type=str, metavar='output_direcotry', nargs='?', default="",
                        help='Output directory for given tileset (default: ($input_dir)_out')
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)




