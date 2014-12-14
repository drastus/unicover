#!/usr/bin/env python3

import re
import sys

from unicover.ranges import Ranges

INB = 'Blocks.txt'
INU = 'UnicodeData.txt'
OUT = 'unicover/blocks.py'

def get_ranges(code_points, large_block=False):
	if large_block:
		code_points = list(range(code_points[0], code_points[1]))
	ranges = Ranges(code_points)
	return ranges.ranges

blocks = []
with open(INB) as in_blocks:
	for line in in_blocks:
		if not line.startswith(('#', '\n')):
			blocks.append(re.split(r'\.\.|; ', line.rstrip()) + [[]])

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

with open(OUT, 'w') as out:
	out.write('blocks = [\n')
	for block in blocks:
		out.write("\t['{0}', '{1}', '{2}', {3}],\n".format(*block))
	out.write(']\n')
