#!/usr/bin/env python3

import os
from setuptools import setup

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = 'UniCover',
	version = '0.1 beta',
	author = 'Michał Górny',
	author_email = 'zrchos@gmail.com',
	description = ('Displays Unicode chars coverage of system fonts'),
	license = 'GNU GPL v3',
	url = 'https://github.com/drastus/unicover',
	packages = ['unicover'],
	long_description = read('README.rst'),
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Natural Language :: English',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Programming Language :: Python :: 3',
	],
	install_requires = ['Python-fontconfig', 'freetype-py'],
	entry_points = {
		'console_scripts': [
			'unicover=unicover.unicover:main',
		],
	},
)
