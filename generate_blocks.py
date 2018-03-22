#!/usr/bin/env python3

import re
import urllib.request

from unicover.ranges import Ranges

INB = 'Blocks.txt'
INU = 'UnicodeData.txt'
OUT = 'unicover/blocks.py'


def download_unicode_files():
    urllib.request.urlretrieve('ftp://www.unicode.org/Public/UNIDATA/Blocks.txt', 'Blocks.txt')
    urllib.request.urlretrieve('ftp://www.unicode.org/Public/UNIDATA/UnicodeData.txt', 'UnicodeData.txt')


def parse_blocks_file():
    blocks = []
    with open(INB) as in_blocks:
        for line in in_blocks:
            if not line.startswith(('#', '\n')):
                blocks.append(re.split(r'\.\.|; ', line.rstrip()) + [[]])
    return blocks


def get_ranges(code_points, large_block=False):
    if large_block:
        code_points = list(range(code_points[0], code_points[1]))
    ranges = Ranges(code_points)
    return ranges.ranges


def build_blocks(blocks):
    large_block = False
    current_block_ix = 0
    block_end_point = int(blocks[current_block_ix][1], 16)
    code_points = []
    with open(INU) as in_uni:
        for line in in_uni:
            if not line.startswith(('#', '\n')):
                data = line.split(';')
                code_point = int(data[0], 16)
                if code_point > block_end_point:
                    blocks[current_block_ix][3] = get_ranges(code_points, large_block)
                    large_block = False
                    current_block_ix += 1
                    block_end_point = int(blocks[current_block_ix][1], 16)
                    code_points = []
                if data[2][0] in {'L', 'M', 'N', 'P', 'S'} or data[2] == 'Zs':
                    code_points.append(code_point)
                    if data[1].endswith(' First>'):
                        large_block = True
    blocks[current_block_ix][3] = get_ranges(code_points, large_block)
    return blocks


def write_blocks(blocks):
    with open(OUT, 'w') as out:
        out.write('blocks = [\n')
        for block in blocks:
            out.write("    ['{0}', '{1}', '{2}', {3}],\n".format(*block))
        out.write(']\n')


def main():
    download_unicode_files()
    blocks = parse_blocks_file()
    blocks = build_blocks(blocks)
    write_blocks(blocks)


if __name__ == '__main__':
    main()
