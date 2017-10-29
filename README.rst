**UniCover** is a simple command-line tool displaying information about Unicode coverage of system fonts. It should work on systems that utilize Fontconfig (Linux and other Unix-like).

Dependencies: Python-fontconfig, freetype-py.

Installation
============

In most cases issuing the following command will be sufficient:

.. code-block:: bash

    pip3 install --user UniCover

If you get an error from Python Fontconfig library, try installing its header files first, eg. for Debian or Ubuntu:

.. code-block:: bash

    sudo apt install libfontconfig1-dev

Usage
=====

Basic usage
-----------

**Display all characters contained given font family or font file**

Returns list of characters grouped by Unicode blocks.

.. code-block:: bash

    unicover -f 'Liberation Sans'
    unicover -f /usr/share/fonts/TTF/LiberationSans-Bold.ttf

    unicover -f 'Liberation Sans' -g    # lists only Unicode blocks
    unicover -f 'Liberation Sans' -o    # omits summary line (total number of characters)

You can discover what fonts are installed in your system using Fontconfig:

.. code-block:: bash

    fc-list : family        # lists font families
    fc-list : file family   # lists font files with families they belong to

**List all system fonts that contain the specified character**

.. code-block:: bash

    unicover -c ₹
    unicover -c 54f6

    unicover -f ₹ -g        # lists only font families
    unicover -f ₹ -o        # omits summary line (total number of fonts)

System fonts summaries
----------------------

**Display all Unicode blocks supported by the system fonts**

.. code-block:: bash

    unicover -g

**List all characters supported by the system fonts**

.. code-block:: bash

    unicover -l
    unicover -gl            # group characters by Unicode block

Note: output will be very long.
