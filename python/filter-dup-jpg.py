# -*- coding: utf-8 -*-

import hashlib
import glob
import os
from os import path
import uuid
from bloom_filter import BloomFilter
import argparse


def file_hash(file_name):
    return hashlib.md5(open(file_name, 'rb').read()).hexdigest()


# avoid same file name in different directories
def gen_file_name(path_name, new_path):
    new_name = str(uuid.uuid1()) + '.' + path_name.split('.')[-1]
    return path.join(new_path, new_name)


def exists(bf, file_name):
    h = file_hash(file_name)
    if h in bf:
        return True
    bf.add(h)
    return False


# TODO: find duplicated files. generate csv recording name mapping between duplicated files
def process(abs_input_dir, int_dir, abs_dup_dir):
    bf = BloomFilter(max_elements=21616, error_rate=0.01)
    with open('mapping.csv', 'w') as m:
        m.write('old-path-name,new-path-name\n')
        for f in glob.glob(path.join(abs_input_dir, '**/*.jpg'), recursive=True):
            int_name = gen_file_name(f, int_dir)
            os.rename(f, int_name)
            dest_name = int_name
            if exists(bf, int_name):
                dest_name = path.join(abs_dup_dir, path.basename(int_name))
                os.rename(int_name, dest_name)
            m.write(int_name + ',' + dest_name + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', dest='input_dir', required=True, type=str,
                        help='input dir containing jpg files')
    parser.add_argument('-o', dest='output_dir', required=True, type=str,
                        help='output dir containing unique jpg files in input dir')
    parser.add_argument('-d', dest='dup_dir', required=True, type=str,
                        help='dup dir containing duplicated jpg files in input dir')
    args = parser.parse_args()
    process(args.input_dir, args.output_dir, args.dup_dir)