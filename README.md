# grep_vcf

[![License (GPL version 3)](https://img.shields.io/badge/license-GNU%20GPL%20version%203-blue.svg?style=flat-square)](https://opensource.org/licenses/GPL-3.0)
[![Build Status](https://travis-ci.org/bneron/grep_vcf.svg?branch=master)](https://travis-ci.org/bneron/grep_vcf)
[![Documentation Status](https://readthedocs.org/projects/grep-vcf/badge/?version=latest)](https://grep-vcf.readthedocs.io/en/latest/?badge=latest)
      
grep_vcf is a tiny tool to filter vcf file based on position file and *vice et versa*.  

<pre>
grep_vcf - filter vcf to keep lines that match positions given in reference file.  

positional arguments:
  positions      The text file with the positions looking for in vcf file. It
                 must be a tsv file (https://en.wikipedia.org/wiki/Tab-separated_values).
                 Where position are in first column.
                 Lines starting with '#' are considering as comments.

optional arguments:
  -h, --help     show this help message and exit
  --vcf VCF      The path to the vcf file. By default grep_vcf search for the
                 same path as position file but with '.vcf' as extension.
  --out OUT      The path to an output file, default is stdout. If the file
                 exists, it will be replaced.
  --invert, -v   Invert the sense of matching, to select non-matching vcf
                 lines.
  --switch       Filter position file to keep lines that position match in vcf
  --version, -V  Display version information and quit.
</pre>

# Installation

```bash
pip install git@https://github.com/bneron/grep_vcf.git#egg=grep_vcf
```

## Documentation

[![Documentation Status](https://readthedocs.org/projects/grep-vcf/badge/?version=latest)](https://grep-vcf.readthedocs.io/en/latest/?badge=latest)

## Licence:

grep_vcf is developed and released under [open source licence GPLv3](https://opensource.org/licenses/GPL-3.0)

## Contributing 

We encourage contributions, bug report, enhancement ... 

But before to do that, we encourage to read [the contributing guide](CONTRIBUTING.md).
