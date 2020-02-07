.. grep_vcf documentation master file, created by
   sphinx-quickstart on Fri Feb  7 10:24:35 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================================
Welcome to grep_vcf's documentation!
====================================

User Guide
==========

grep_vcf is a tiny tool to filter vcf file based on position file and *vice et versa*.
The position file must be a tabulated file with a genomic position as first column.
This tool is designed to support big files without consuming huge memory.

Usage
-----

**positional arguments:**
  positions      The text file with the positions looking for in vcf file. It
                 must be a tsv file (https://en.wikipedia.org/wiki/Tab-
                 separated_values).where position are in first column.Lines
                 starting with '#' are considering as comments.

**optional arguments:**
  -h, --help     show this help message and exit
  --vcf VCF      The path to the vcf file. By default grep_vcf search for the
                 same path as position file but with '.vcf' as extension.
  --out OUT      The path to an output file, default is stdout. If the file
                 exists, it will be replaced.
  --invert, -v   Invert the sense of matching, to select non-matching vcf
                 lines.
  --switch       Filter position file to keep lines that position match in vcf
  --version, -V  Display version information and quit.


Requirements
------------

`grep_vcf` need python >= 3.6 (tested with 3.6, 3.7 3.8)


Installation
------------

::

   pip install git@https://github.com/bneron/grep_vcf.git#egg=grep_vcf



Developer Guide
===============

Installation
------------

The recommend way to install grep_vcf is to use a virtualenv::

   python -m venv grep_vcf
   cd grep_vcf
   source bin/activate
   git clone https://github.com/bneron/grep_vcf.git
   cd grep_vcf
   pip install -e .[dev]


Overview
--------

There are 2 main files
   * `grep_vcf/grep_vcf.py`  which is the module
   * `grep_vcf/scripts/grep_vcf.py` which is the entrypoint to run grep_vcf from command line.

API
---

Module API
----------

The module contains mainly two functions

   * `match_generator` that allow to keep lines with a given position in target file based
      on position found in reference file.
   * `invert_match_generator which` that allow to filter out lines with a given position in target file based
      on position found in reference file.

These tow functions are `generators` to try to work in constant memory even with big files.

.. note::
   in both cases line starting with `#` are considering as comments and are ignored.

The other functions are helpers.



.. automodule:: grep_vcf.grep_vcf
   :members:
   :private-members:
   :special-members:

Scripts API
-----------


.. automodule:: grep_vcf.scripts.grep_vcf
   :members:
   :private-members:
   :special-members:


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
