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
import os
import shutil
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove


X = 0
Y = 1
DX = 2
DY = 3
PB = 4
SX = 5
SY = 6
TNAME = 7

tiles_list = list()
sizes = [0, 0, 0, 0, 0]  # x,y,dx, dy, pb


def load_dir(dir_name):
    global tiles_list
    files = []
    for file in os.listdir(dir_name):
        if file.endswith(".spec"):
            print("Loading", file)
            tiles_list = list()
            load_spec(dir_name + os.path.sep + file)

# global sizes get overwritten depending on section


def extract_size(line):
    global sizes
    if ('=' not in line):
        return
    left, right = line.split('=')
    left = left.strip()
    right = right.strip()

    if left == "tiles":
        return 1

    if left == 'x_top_left':
        sizes[X] = right
    if left == 'y_top_left':
        sizes[Y] = right
    if left == 'dx':
        sizes[DX] = right
    if left == 'dy':
        sizes[DY] = right
    if left == 'pixel_border':
        sizes[PB] = right


def extract_filename(line):
    if ('=' not in line):
        return
    left, right = line.split('=')
    left = left.strip()
    right = right.strip()
    if (left == 'gfx'):
        return right


def extract_tiles(line):
    global tiles_list
    line = line.strip()
    tile_list = line.split(',')

    if len(tile_list) < 3:
        return
    s = sizes.copy()
    s.extend(tile_list)

    ds = list(map(int, s[0:TNAME]))
    ds.append(s[TNAME].strip())

    tiles_list.append(ds)


def load_spec(filename, output_dir):
    lineNumber = 0

    where = "nowhere"
    file = str()
    global sizes

    sizes = [0, 0, 0, 0, 0]  # x,y,dx, dy, pb

    # try: or dont even try
    with open(filename, "r") as reader:
        all = reader.readlines()

        while True:
            if (len(all)) == 0:
                break
            line = all.pop(0)
            line = line.strip()

            if not line:
                continue

            if line[0] == ";" or line[0] == "}":
                continue

            # remove comments
            if ";" in line:
                x = line.find(";")
                line = line[0:x]

            if (line[0] == "["):
                where = line
                if ("grid" in where):
                    where = "[grid]"
                continue

            if (where == "[file]"):
                f = extract_filename(line)
                if (f):
                    filename = f
                    print("FILENAME:", f)

            # tiles is non existent section that should exist
            # if tiles are not row, column, tag then gg
            if (where == "[tiles]"):
                f = extract_tiles(line)
                continue

            if (where == "[grid]"):
                x = extract_size(line)
                # gate to invisible section
                if x:
                    where = "[tiles]"

            if (where == "[in_the_hell]"):
                continue

            lineNumber += 1

    reader.close()
    load_image(filename, output_dir)

    # except:
    #     err = sys.exc_info()[0]
    #     print(f"Error ***{err}*** when reading file {filename}. Exiting")
    #     exit(1)


def load_image(filename, output_dir):

    box = tuple()
    filename = filename.replace("\"", "") + ".png"
    im = Image.open(filename)

    imsize = im.size
    im_mod = Image.new("RGBA", imsize, "black")

    for tile in tiles_list:
        # Did u see this this coming ?
        box = (tile[Y] + tile[DX] * tile[SY] + tile[PB] * tile[SY],
               tile[X] + tile[DY] * tile[SX] + tile[PB] * tile[SX],
               tile[Y] + tile[DX] * tile[SY] + tile[DX] + tile[PB] * tile[SY],
               tile[X] + tile[DY] * tile[SX] + tile[DY] + tile[PB] * tile[SX])

        region = im.crop(box)
        im_mod.paste(region, box)

    bad_deadpool, good_deadpool = os.path.split(filename)
    print(f"Writing:{good_deadpool} to {output_dir}" )
    im_mod.save(output_dir + os.path.sep + good_deadpool)


def load_tileset(input_file):
    (eiskalt, erwischt) = os.path.splitext(input_file)
    load_dir(eiskalt)


def write_tilespec(filew, inputr):
    output_specfile = filew + ".tilespec"
    inr = inputr + ".tilespec"
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(inr) as old_file:
            for line in old_file:
                if "name =" in line:
                    shock = "name = \"" + filew + "\"\n"
                    new_file.write(shock)
                    continue
                if inputr in line and ".spec" in line:
                    # it will work!!! (maybe)
                    a1 = line.find("\"")
                    a2 = line.rfind("/")
                    newline = line[:a1] + "\"" + filew + line[a2:]
                    new_file.write(newline)
                    continue
                new_file.write(line)
    # Remove original file
    if os.path.isfile(output_specfile):
        remove(output_specfile)
    # Move new file
    move(abs_path, output_specfile)


def write_directory(output_file, input):
    global tiles_list
    files = []

    if os.path.isdir(output_file):
        shutil.rmtree(output_file)
    os.mkdir(output_file)

    for filex in os.listdir(input):
        if filex.endswith(".spec"):
            print("Loading", filex)
            tiles_list = list()
            load_spec(input + os.path.sep + filex, output_file)
            output_specfile = output_file + os.path.sep + filex

            fh, abs_path = mkstemp()
            filex = input + os.path.sep + filex
            with fdopen(fh, 'w') as new_file:
                with open(filex) as old_file:
                    for line in old_file:
                        if "gfx = " in line or "gfx=" in line:
                            a1 = line.find("\"")
                            a2 = line.rfind("/")
                            newline = line[:a1] + "\"" + \
                                output_file + line[a2:]
                            new_file.write(newline)
                            continue
                        new_file.write(line)

            # Remove original file
            if os.path.isfile(output_specfile):
                remove(output_specfile)
            # Move new file
            move(abs_path, output_specfile)


def write_tileset(input_file, output_file):
    (miststuck, eiskalt) = os.path.splitext(input_file)
    write_tilespec(output_file, miststuck)
    write_directory(output_file, miststuck)


def main(input_file, output_file):
    # load_tileset(input_file)
    write_tileset(input_file, output_file)


if __name__ == '__main__':
    parser = ArgumentParser(description='Freeciv Tileset Modifier')
    parser.add_argument('input_tilespec', nargs='?', default='trident.tilespec',
                        help='Tileset file (default: %(default)s)')
    parser.add_argument('-output_file', type=str, metavar='string', nargs='?', default="XXX",
                        help='New tileset name (default: ($output_file), "\
                             "directory with that name will be wiped, you have been warned')
    args = parser.parse_args()
    main(args.input_tilespec, args.output_file)
