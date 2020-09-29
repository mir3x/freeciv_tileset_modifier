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
from PIL import Image
from argparse import ArgumentParser

def load_dir(dir_name):
    load_spec("XXX")

def load_spec(filename):
    try:
        with open("trident/tiles.spec", "r") as reader:
            all = reader.readlines()
            while True:

                if (len(all)) == 0:
                    break
                line = all.pop(0)
        reader.close()

    except:
        err = sys.exc_info()[0]
        print(f"Error ***{err}*** when reading file {filename}. Exiting")
        exit(1)

def load_image(filename):
    im = Image.open("trident/tiles.png")
    pass

def save_spec(filename):
    pass

def load_img(filename):
    pass

def main(input_dir, output_dir):
    load_dir(input_dir)

if __name__ == '__main__':
    parser = ArgumentParser(description='Freeciv Tileset Modifier')
    parser.add_argument('input_dir', nargs='?', default='trident',
                        help='Tileset directory (default: %(default)s)')
    parser.add_argument('-output_dir', type=str, metavar='output_direcotry', nargs='?', default="",
                        help='Output directory for given tileset (default: ($input_dir)_out')
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)




