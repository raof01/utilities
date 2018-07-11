# -*- coding: utf-8 -*-

import hashlib
import fnmatch
import os
from os import path
import uuid
from bloom_filter import BloomFilter
import argparse
import tqdm


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
def process(abs_input_dir, abs_dup_dir):
    bf = BloomFilter(max_elements=21616 * 2, error_rate=0.01)
    with open('mapping.csv', 'w') as m:
        m.write('old-path-name,new-path-name\n')
        files = [v for v in os.walk(abs_input_dir)]
        for f in tqdm.tqdm(files):
            for b in tqdm.tqdm(f[2]):
                if fnmatch.fnmatch(b, '*.jpg'):
                    name = path.join(f[0], b)
                    if exists(bf, name):
                        dest_name = gen_file_name(name, abs_dup_dir)
                        #print('os.rename('+ name + ', ' + dest_name + ')')
                        os.rename(name, dest_name)
                        m.write(name + ',' + dest_name + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', dest='input_dir', required=True, type=str,
                        help='input dir containing jpg files')
    parser.add_argument('-d', dest='dup_dir', required=True, type=str,
                        help='dup dir containing duplicated jpg files in input dir')
    args = parser.parse_args()
    process(args.input_dir, args.dup_dir)
