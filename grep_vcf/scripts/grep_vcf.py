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
    parser = argparse.ArgumentParser()

    parser.add_argument("positions")
    parser.add_argument("--vcf",
                        help="the path to the vcf file by default the same path as position file "
                             "but with '.vcf' as extension"
                        )
    parser.add_argument("--out",
                        default=sys.stdout,
                        help="the path to an output file, default is stdout")
    parsed_args = parser.parse_args(args)

    for path in text_path, vcf_path:
        if not os.path.exists(vcf_path):
            raise FileNotFoundError(f"the file {path} does not exists.")

    return parsed_args


def main(args=None):
    args = sys.argv[1:] if args is None else args
    parsed_args = parse_args(args)

    text_path = parsed_args.positions
    vcf_path = parsed_args.vcf

    with open(text_path) as text, open(vcf_path) as vcf:
        for line in gv.diff_generator(text, vcf):
            print(line, end="", file=parsed_args.out)


if __name__ == "__main__":
    main()
