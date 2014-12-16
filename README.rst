**UniCover** is a simple command-line tool displaying information about Unicode coverage of system fonts. It should work on systems that utilize Fontconfig (Linux and other Unix-like).

Dependencies: python-fontconfig, freetype-py.

Basic usage
===========

.. code-block:: bash
	unicover -f font_file
or
.. code-block:: bash
	unicover -f font_family
displays character coverage of given font file or font family.

.. code-block:: bash
	unicover -c character
or
.. code-block:: bash
	unicover -c character_hex_code
lists all system fonts that contain the specified character.

To display all Unicode blocks supported by system fonts, type:
.. code-block:: bash
	unicover -g
To list all characters supported by system fonts (output will be very long), type:
.. code-block:: bash
	unicover -l
It is also possible to combine these two options:
.. code-block:: bash
	unicover -gl
