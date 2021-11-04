##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##
##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##
##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##
##=##=##=# You are not meant to understand this ##=##=##=##=##
##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##
##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##
##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##

import os
import shutil
import sys
import traceback
from argparse import ArgumentParser
from os import fdopen, remove
from shutil import move
from tempfile import mkstemp

from PIL import Image

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
scale = 100
is_overhead = False

def remove_comments(line):
    if (";" in line):
        x = line.find(";")
        line = line[0:x]
    return line

def load_dir(dir_name):
    global tiles_list
    files = []
    for file in os.listdir(dir_name):
        if file.endswith(".spec"):
            print("Loading", file)
            tiles_list = list()
            load_spec(dir_name + os.path.sep + file)

# writes to global sizes, get overwritten depending on section
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

    try:
        with open(filename, "r") as reader:
            speciman_file = reader.readlines()

            while True:
                if not speciman_file:
                    break
                line = speciman_file.pop(0)
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
                    # if you are here you are doomed
                    continue

                lineNumber += 1

        reader.close()
    except:
        err = sys.exc_info()[0]
        print(f"\033[91mError ***{err}*** when reading file {self.filename}. Exiting\033[0m")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        exit(1)
    load_image(filename, output_dir)

    # except:
    #     err = sys.exc_info()[0]
    #     print(f"Error ***{err}*** when reading file {filename}. Exiting")
    #     exit(1)

def sc_v(val):
    global scale
    return int(val * scale /100)

def load_image(filename, output_dir):
    global scale
    box = tuple()
    filename = filename.replace("\"", "") + ".png"
    im = Image.open(filename)

    imsize = im.size
    newsize = (sc_v(im.size[0]), sc_v(im.size[1]))
    im_mod = Image.new("RGBA", newsize, "black")

    for tile in tiles_list:
        # Could u see this this coming ?
        box = (tile[X] + tile[DX] * tile[SY] + tile[PB] * tile[SY],
               tile[Y] + tile[DY] * tile[SX] + tile[PB] * tile[SX],
               tile[X] + tile[DX] * tile[SY] + tile[DX] + tile[PB] * tile[SY],
               tile[Y] + tile[DY] * tile[SX] + tile[DY] + tile[PB] * tile[SX])

        region = im.crop(box)
        new_region = region.resize((sc_v(region.size[0]), sc_v(region.size[1])), Image.BOX)
        # scaling
        tile[X] = sc_v(tile[X])
        tile[Y] = sc_v(tile[Y])
        tile[DY] = sc_v(tile[DY])
        tile[DX] = sc_v(tile[DX])
        tile[PB] = sc_v(tile[PB])
        newbox = (tile[X] + tile[DX] * tile[SY] + tile[PB] * tile[SY],
                  tile[Y] + tile[DY] * tile[SX] + tile[PB] * tile[SX],
                  tile[X] + tile[DX] * tile[SY] + tile[DX] + tile[PB] * tile[SY],
                  tile[Y] + tile[DY] * tile[SX] + tile[DY] + tile[PB] * tile[SX])
        im_mod.paste(new_region, newbox)

    bad_deadpool, good_deadpool = os.path.split(filename)
    print(f"Writing:{output_dir}{os.path.sep}{good_deadpool}")
    im_mod.save(output_dir + os.path.sep + good_deadpool)


def load_tileset(input_file):
    (eiskalt, erwischt) = os.path.splitext(input_file)
    load_dir(eiskalt)

def replace_line_with_scale(line):
    global scale
    line = remove_comments(line)
    newline = line
    something = ["normal_tile_width", "normal_tile_height",
                 "small_tile_width", "small_tile_height"]

    for anything in something:
        if anything in line:
            left, right = line.split('=')
            tostr_toint_scaledright = str(sc_v(int(right)))
            newline = " ".join([left, "=", tostr_toint_scaledright, "\n"])

    return newline

# its the same JUST CAUSE
def replace_line_grid_scale(line):
    global scale
    line = remove_comments(line)
    newline = line
    something = ["x_top_left", "y_top_left", "pixel_border",
                 "dx", "dy", ]

    for anything in something:
        if anything in line:
            left, right = line.split('=')
            tostr_toint_scaledright = str(sc_v(int(right)))
            newline = " ".join([left, "=", tostr_toint_scaledright, "\n"])

    return newline

def write_tilespec(filew, inputr):
    global scale
    global is_overhead
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

                if "type" in line and "overhead" in line and "=" in line:
                    is_overhead = True;


                if (scale != 100):
                    newline = replace_line_with_scale(line)
                    new_file.write(newline)
                    continue
                new_file.write(line)
    # Remove original file
    if os.path.isfile(output_specfile):
        remove(output_specfile)
    # Move new file
    move(abs_path, output_specfile)
    print(f"Writing:{output_specfile}")


def write_directory(output_file, input):
    global tiles_list
    global scale
    files = []
    where = "notgrid"
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
                        if line[0] == "[":
                            if "[grid_" in line:
                                where = "grid"
                            else:
                                where = "notgrid"

                        if where == "grid" and scale !=100:
                            newline = replace_line_grid_scale(line)
                            new_file.write(newline)
                            continue

                        new_file.write(line)



            # Remove original file
            if os.path.isfile(output_specfile):
                remove(output_specfile)
            # Move new file
            move(abs_path, output_specfile)
            print(f"Writing:{output_specfile}")


def write_tileset(input_file, output_file):
    (miststuck, eiskalt) = os.path.splitext(input_file)
    write_tilespec(output_file, miststuck)
    write_directory(output_file, miststuck)


def main(input_file, output_file, scalpel):
    # load_tileset(input_file)
    global scale
    scale = scalpel

    write_tileset(input_file, output_file)



if __name__ == '__main__':
    parser = ArgumentParser(description='Freeciv Tileset Modifier')
    parser.add_argument('input_tilespec', nargs='?', default='trident.tilespec',
                        help='Tileset file (default: %(default)s)')
    parser.add_argument('-output_file', type=str, metavar='string', nargs='?', default="XXX",
                        help='New tileset name (default: ($output_file), "\
                             "directory with that name will be wiped, you have been warned')
    parser.add_argument('-scale', type=int, metavar='percent', nargs='?', default="200",
                        help='New scale in percent (default: ($scale) ')
    args = parser.parse_args()
    main(args.input_tilespec, args.output_file, args.scale)
