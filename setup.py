#!/usr/bin/env python3

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='UniCover',
    version='0.1',
    author='Michał Górny',
    author_email='zrchos@gmail.com',
    description=('Displays Unicode chars coverage of system fonts'),
    license='MIT',
    url='https://github.com/drastus/unicover',
    packages=['unicover'],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Console Fonts',
        'Topic :: Text Processing :: Fonts',
        'Topic :: Utilities',
    ],
    install_requires=['Python-fontconfig', 'freetype-py'],
    entry_points={
        'console_scripts': [
            'unicover=unicover.unicover:main',
        ],
    },
)
