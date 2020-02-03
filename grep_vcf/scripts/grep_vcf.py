#########################################################################
# grep_vcf - remove line fom vcf file where positions are not in        #
# reference file                                                        #
# Authors: Bertrand Neron                                               #
# Copyright (c) 2020  Institut Pasteur (Paris) and CNRS.                #
# See the COPYRIGHT file for details                                    #
#                                                                       #
# This file is part of grep_vcf package.                                #
#                                                                       #
# grep_vcf is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# grep_vcf is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
# GNU General Public License for more details .                         #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with MacSyFinder (COPYING).                                     #
# If not, see <https://www.gnu.org/licenses/>.                          #
#########################################################################

import sys
import os
import argparse
import grep_vcf
import grep_vcf.grep_vcf as gv


def get_version_message():
    """
    :return: the version informations
    :rtype: str
    """
    version = grep_vcf.__version__
    vers_msg = f"""grep_vcf {version}
Python {sys.version}

grep_vcf is distributed under the terms of the GNU General Public License (GPLv3).
See the COPYING file for details.
"""
    return vers_msg


def parse_args(args):
    """

    :param args: The arguments provided on the command line
    :type args: List of strings [without the program name]
    :return: The arguments parsed
    :rtype: :class:`aprgparse.Namespace` object.
    """
    parser = argparse.ArgumentParser(
        epilog="For more details, visit the MacSyFinder website and see the MacSyFinder documentation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""

grep_vcf - filter vcf to keep line at given positions.  
""")

    parser.add_argument("positions",
                        help="The text file with the position to keep. "
                             "It must be a tsv file where position are in first col."
                             "lines starting with '#' are comments.")
    parser.add_argument("--vcf",
                        help="the path to the vcf file by default the same path as position file "
                             "but with '.vcf' as extension."
                        )
    parser.add_argument("--out",
                        default=sys.stdout,
                        help="the path to an output file, default is stdout."
                             "if the file exists, it will be replaced")
    parser.add_argument("--version",
                        action='version',
                        version=get_version_message(),
                        help="display version information and quit."
                        )
    parsed_args = parser.parse_args(args)

    if parsed_args.vcf is None:
        parsed_args.vcf = os.palth.splitext(parsed_args.positions)[0] + '.vcf'

    for path in parsed_args.positions, parsed_args.vcf:
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exists.")

    return parsed_args


def main(args=None):
    """

    :param args: the arguments to use to run
    :param args: list of str
    """
    args = sys.argv[1:] if args is None else args
    parsed_args = parse_args(args)

    positions_path = parsed_args.positions
    vcf_path = parsed_args.vcf

    if parsed_args.out is not sys.stdout:
        out = open(parsed_args.out, 'w')
    else:
        out = sys.stdout

    try:
        with open(positions_path) as positions, open(vcf_path) as vcf:
            for line in gv.diff_generator(positions, vcf):
                out.write(line)
    finally:
        if not out.closed and out.name != '<stdout>':
            out.close()


if __name__ == "__main__":
    main()
