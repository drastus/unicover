#!/usr/bin/env python3
#
# UniCover 0.1 β
#
# © 2014 Michał Górny
# Distributed under the terms of the GNU General Public License v3.
# See http://www.gnu.org/licenses/gpl.txt for the full license text.
#
# Displays info about characters supported by fonts.

import argparse
import os.path
import string
import sys
from collections import defaultdict
from operator import itemgetter

import fontconfig as fc
import freetype as ft
import unicodedata as ud

from .blocks import blocks as all_blocks
from .ranges import Ranges


class UniCover:
	"""
	UniCover 0.1 beta.
	Displays info about characters supported by fonts.
	"""

	def __init__(self):
		self._display = {}

	def start(self):
		try:
			args = self.parse_args()
			self.dispatch(args)
		except (ValueError, ft.ft_errors.FT_Exception) as error:
			print(error)

	def parse_args(self):
		ap = argparse.ArgumentParser(
			description=self.__doc__
		)
		ap.add_argument('-f', '--font', help='specify font (file path or font family name)')
		group = ap.add_mutually_exclusive_group()
		group.add_argument('-c', '--char', help='specify character (literal or hex Unicode number)')
		group.add_argument('-b', '--block', help='specify Unicode block (name or hex Unicode number of start code point)')
		ap.add_argument('-l', '--list', action='store_true', help='show list of characters or font files')
		ap.add_argument('-g', '--group', action='store_true', help='show groups of characters or fonts')
		ap.add_argument('-o', '--omit-summary', action='store_true', help='omit summary')
		return ap.parse_args()

	def dispatch(self, args):
		"""
		Calls proper method depending on command-line arguments.
		"""
		if not args.list and not args.group:
			if not args.font and not args.char and not args.block:
				self.info()
				return
			else:
				args.list = args.group = True
		self._display = {k: args.__dict__[k] for k in ('list', 'group', 'omit_summary')}
		if args.char:
			char = self._getChar(args.char)
			if args.font:
				self.fontChar(args.font, char)
			else:
				self.char(char)
		else:
			block = self._getBlock(args.block)
			self.chars(args.font, block)

	def info(self):
		"""
		Displays basic info on UniCover.
		"""
		print(self.__doc__)
		print('Type unicover -h for help.')

	def chars(self, font, block):
		"""
		Analyses characters in single font or all fonts.
		"""
		if font:
			font_files = self._getFont(font)
		else:
			font_files = fc.query()
		code_points = self._getFontChars(font_files)

		if not block:
			blocks = all_blocks
			ranges_column = map(itemgetter(3), blocks)
			overlapped = Ranges(code_points).getOverlappedList(ranges_column)
		else:
			blocks = [block]
			overlapped = [Ranges(code_points).getOverlapped(block[3])]

		if self._display['group']:
			char_count = block_count = 0
			for i, block in enumerate(blocks):
				o_count = len(overlapped[i])
				if o_count:
					block_count += 1
					char_count += o_count
					total = sum(len(r) for r in block[3])
					percent = 0 if total==0 else o_count/total
					print("{0:>6}  {1:47} {2:>4.0%} ({3}/{4})".format(block[0], block[2], percent, o_count, total))
					if self._display['list']:
						for point in overlapped[i]:
							print('{0:0>4X} '.format(point).rjust(9), ud.name(chr(point), '<code point {0:0>4X}>'.format(point)))
			self._charSummary(char_count, block_count)
		else:
			for point in code_points:
				print('{0:0>4X} '.format(point).rjust(7), ud.name(chr(point), '<code point {0:0>4X}>'.format(point)))
			self._charSummary(len(code_points))

	def char(self, char):
		"""
		Shows all system fonts that contain given character.
		"""
		font_files = fc.query()
		if self._display['group']:
			font_files = self._getFontChar(font_files, char)
			font_families = self._groupFontByFamily(font_files)
			for font_family in sorted(font_families):
				print(font_family)
				if self._display['list']:
					for font_file in font_families[font_family]:
						print('  '+font_file)
			self._fontSummary(len(font_files), len(font_families))
		else:
			font_files = self._getFontChar(font_files, char)
			for font_file in sorted(font_files):
				print(font_file)
			self._fontSummary(len(font_files))

	def fontChar(self, font, char):
		"""
		Checks if characters occurs in the given font.
		"""
		font_files = self._getFontChar(self._getFont(font), char)
		print('The character is {0}present in this font.'.format('' if font_files else 'not '))


	def _charSummary(self, char_count, block_count=None):
		if not self._display['omit_summary']:
			if block_count is None:
				print('Total code points:', char_count)
			else:
				print('Total {0} code point{1} in {2} block{3}'.format(
					char_count,
					's' if char_count!=1 else '',
					block_count,
					's' if block_count!=1 else ''
				))

	def _fontSummary(self, font_file_count, font_family_count=None):
		if not self._display['omit_summary']:
			if font_family_count is None:
				print('Total font files:', font_file_count)
			else:
				print('The character is present in {0} font file{1} and {2} font famil{3}'.format(
					font_file_count,
					's' if font_file_count!=1 else '',
					font_family_count,
					'ies' if font_family_count!=1 else 'y'
				))

	def _getChar(self, char_spec):
		if len(char_spec) >= 4 and all(c in string.hexdigits for c in char_spec):
			char_number = int(char_spec, 16)
			if char_number not in range(0x110000):
				raise ValueError('No such character')
			return chr(char_number)
		elif len(char_spec) == 1:
			return char_spec
		else:
			raise ValueError('No such character')

	def _getBlock(self, block_spec):
		if block_spec is None:
			return
		if all(c in string.hexdigits for c in block_spec):
			block_spec = block_spec.upper()
			ix = 0
		else:
			ix = 2
		for block in all_blocks:
			if block[ix] == block_spec:
				return block
		raise ValueError('No such block')

	def _getFont(self, font):
		if os.path.isfile(font):
			font_files = [font]
		else:
			font_files = fc.query(family=font)
			if not font_files:
				raise ValueError('No such font')
		return font_files

	def _getFontChars(self, font_files):
		code_points = set()
		for font_file in font_files:
			face = ft.Face(font_file)
			charcode, agindex = face.get_first_char()
			while agindex != 0:
				code_points.add(charcode)
				charcode, agindex = face.get_next_char(charcode, agindex)
		return sorted(code_points)

	def _getFontChar(self, font_files, code_point):
		return_font_files = []
		for font_file in font_files:
			face = ft.Face(font_file)
			if face.get_char_index(code_point):
				return_font_files.append(font_file)
		return return_font_files

	def _groupFontByFamily(self, font_files):
		font_families = defaultdict(list)
		for font_file in font_files:
			font = fc.FcFont(font_file)
			font_families[font.family[0][1]].append(font_file)
		return font_families


def main():
	UniCover().start()


if __name__=='__main__':
	main()
