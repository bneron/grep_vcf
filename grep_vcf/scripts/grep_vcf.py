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
# along with grep_vcf (LICENSE).                                        #
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
        epilog="For more details, visit the grep vcf github page and see the grep vcf documentation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
  _____                 __      _______ ______ 
 / ____|                \ \    / / ____|  ____|
| |  __ _ __ ___ _ __    \ \  / / |    | |__   
| | |_ | '__/ _ \ '_ \    \ \/ /| |    |  __|  
| |__| | | |  __/ |_) |    \  / | |____| |     
 \_____|_|  \___| .__/      \/   \_____|_|     
                | |                            
                |_|                            

grep_vcf - filter vcf to keep lines that match positions given in reference file.  
""")

    parser.add_argument("positions",
                        help="The text file with the positions looking for in vcf file. "
                             "It must be a tsv file (https://en.wikipedia.org/wiki/Tab-separated_values)."
                             "where position are in first column."
                             "Lines starting with '#' are considering as comments.")
    parser.add_argument("--vcf",
                        help="The path to the vcf file. By default grep_vcf search for the same path as position file"
                             " but with '.vcf' as extension."
                        )
    parser.add_argument("--out",
                        default=sys.stdout,
                        help="The path to an output file, default is stdout. "
                             "If the file exists, it will be replaced.")
    parser.add_argument("--invert", "-v",
                        action='store_true',
                        default=False,
                        help="Invert the sense of matching, to select non-matching vcf lines.")
    parser.add_argument("--switch",
                        action='store_true',
                        default=False,
                        help="Filter position file to keep lines that position match in vcf")
    parser.add_argument("--version", "-V",
                        action='version',
                        version=get_version_message(),
                        help="Display version information and quit."
                        )
    parsed_args = parser.parse_args(args)

    if parsed_args.vcf is None:
        parsed_args.vcf = os.path.splitext(parsed_args.positions)[0] + '.vcf'

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
            ref, target = (positions, vcf) if not parsed_args.switch else (vcf, positions)
            if parsed_args.invert:
                gen = gv.invert_match_generator(ref, target)
            else:
                gen = gv.match_generator(ref, target)

            for line in gen:
                out.write(line)
    finally:
        if not out.closed and out.name != '<stdout>':
            out.close()


if __name__ == "__main__":
    main()
