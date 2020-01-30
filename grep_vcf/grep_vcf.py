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

__version__ = 0.1


def _parse_line(file):
    """
    Go to next line and parse it, extract the first field and transform it in int.
    Ignore comments (line starting with #)

    :param file: the file to parse
    :type file: a file object
    :return: the position parsed
    :rtype: int
    :raise StopIteration: when reach the end of file
    """
    line = next(file)
    while line.startswith('#'):
        line = next(file)
    else:
        current_pos = int(line.split()[0])
    return current_pos, line


def diff_generator(txt_file, vcf_file):
    """
    create a generator which can iterate over line in vcf
    where position not appear in text file
    the position are extract from the first column of text_file and vcf_file.

    .. _warning:
        the position in the text_file and vcf_file must be sorted (ascending)

    :param txt_file: the text file to extract
    :type txt_file: file object
    :param vcf_file: the vcf to compare
    :type vcf_file: file object
    :return: a generator
    :rtype: generator
    """
    txt_pos, line = _parse_line(txt_file)
    vcf_pos, _ = _parse_line(vcf_file)
    vcf_end = False
    txt_end = False
    while True:
        if txt_pos == vcf_pos:
            try:
                vcf_pos, _ = _parse_line(vcf_file)
            except StopIteration:
                vcf_end = True
            try:
                txt_pos, line = _parse_line(txt_file)
            except StopIteration:
                txt_end = True
        elif txt_pos > vcf_pos:
            try:
                vcf_pos, _ = _parse_line(vcf_file)
            except StopIteration:
                vcf_end = True
        else:  # txt_pos < vcf_pos
            yield line
            try:
                txt_pos, line = _parse_line(txt_file)
            except StopIteration:
                txt_end = True
        if txt_end:
            break
        if vcf_end:
            yield line
            for line in txt_file:
                _, line = _parse_line(line)  # to remove comment
                yield line

