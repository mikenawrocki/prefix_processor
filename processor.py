#!/usr/bin/env python3
import configparser
import os
import shutil
import sys

# Use the first 3 characters as the pattern.
MATCH_LEN = 3

# Maps the first MATCH_LEN characters of a filename to a desired directory.
dir_map = { }

# Do not map the script or configuration file.
exclude_list = [ os.path.basename(__file__), 'processor_mapping.ini' ]

def fill_dir_map():
    global dir_map
    config = configparser.ConfigParser()
    config.read('processor_mapping.ini')
    dir_map = { k:v for k,v in config.items('DIRS') }

def verify_map_dirs():
    for d in dir_map.values():
        if not os.path.isdir(d):
            raise IOError("%s is not a valid directory!" % d)

def find_new_path(dest_path, files):
    dir_path = os.path.dirname(dest_path)
    dest_relname = os.path.basename(dest_path)
    new_name, ext = os.path.splitext(dest_relname)
    
    num_ext = 1
    possible_new_name = "{0}.{1:04d}{2}".format(new_name, num_ext, ext)
    possible_path = os.path.join(dir_path, possible_new_name)
    while os.path.exists(possible_path):
        num_ext += 1
        possible_new_name = "{0}.{1:04d}{2}".format(new_name, num_ext, ext)
        possible_path = os.path.join(dir_path, possible_new_name)

    return possible_path

def main(argv):
    files = [fp for fp in os.listdir('.') if os.path.isfile(fp)]
    fill_dir_map()
    verify_map_dirs()
    for fp in files:
        try:
            if fp not in exclude_list:
                dest_path = os.path.join(dir_map[fp[0:MATCH_LEN].lower()], fp)
                if not os.path.exists(dest_path):
                    print("Moving file {} to directory {}".format(fp, dest_path))
                    shutil.move(fp, dest_path)
                else:
                    mod_dest_path = find_new_path(dest_path, files)
                    print("File {} exists! Moving {} to {}".format(dest_path,fp,
                                                            mod_dest_path))
                    shutil.move(fp, mod_dest_path)
        except KeyError:
            print("Error! No mapping found for %s (using %s)" %
                    (fp, fp[0:MATCH_LEN].lower()))

if __name__ == "__main__":
    main(sys.argv[1:])
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
