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

    :param file: the file to parse.
                 it must be a tsv file with an integer as first column.
    :type file: a file object
    :return: the position parsed
    :rtype: int
    :raise StopIteration: when reach the end of file
    :raise ValueError: when first column can not be cast in an integer
    """
    line = next(file).lstrip()
    while line.startswith('#') or not line:
        line = next(file).lstrip()
    else:
        try:
            current_pos = int(line.split()[0])
        except ValueError as err:
            line = line.rstrip('\n')
            raise ValueError(f"{line}: {err}")
    return current_pos, line


def _until_the_end(file):
    """
    Iterate over lines until the end of file.
    Skip line starting with '#'

    :param file: the file to iterate over
    :return: lines
    :rtype: str
    """
    while file:
        try:
            _, line = _parse_line(file)  # to remove comment
            yield line
        except StopIteration:
            break


def match_generator(txt_file, vcf_file):
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
    try:
        txt_pos, _ = _parse_line(txt_file)
        txt_end = False
    except StopIteration:
        txt_end = True
    except ValueError as err:
        raise ValueError(f"position file has wrong format: {err}") from None
    try:
        vcf_pos, line = _parse_line(vcf_file)
        vcf_end = False
    except StopIteration:
        vcf_end = True
    except ValueError as err:
        raise ValueError(f"vcf has wrong format: {err}") from None

    # treat limit cases
    # when a file or both are empty
    if vcf_end or txt_end:
        return
    else:
        while True:
            try:
                if txt_pos == vcf_pos:
                    yield line
                    try:
                        vcf_pos, line = _parse_line(vcf_file)
                    except ValueError as err:
                        raise ValueError(f"vcf has wrong line: {err}") from None
                    try:
                        txt_pos, _ = _parse_line(txt_file)
                    except ValueError as err:
                        raise ValueError(f"position file has wrong format: {err}") from None
                elif txt_pos > vcf_pos:
                    try:
                        vcf_pos, line = _parse_line(vcf_file)
                    except ValueError as err:
                        raise ValueError(f"vcf has wrong line: {err}") from None
                else:  # txt_pos < vcf_pos
                    try:
                        txt_pos, _ = _parse_line(txt_file)
                    except ValueError as err:
                        raise ValueError(f"position file has wrong format: {err}") from None
            except StopIteration:
                break


def invert_match_generator(txt_file, vcf_file):
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
    try:
        txt_pos, _ = _parse_line(txt_file)
        txt_end = False
    except StopIteration:
        txt_end = True
    except ValueError as err:
        raise ValueError(f"position file has wrong format: {err}")
    try:
        vcf_pos, line = _parse_line(vcf_file)
        vcf_end = False
    except StopIteration:
        vcf_end = True
    except ValueError as err:
        raise ValueError(f"vcf has wrong format: {err}")

    # treat limit cases
    # when a file or both are empty
    if vcf_end:
        return
    elif txt_end and not vcf_end:
        yield line
        for line in _until_the_end(vcf_file):
            yield line
    else:
        while True:
            if txt_pos == vcf_pos:
                try:
                    vcf_pos, line = _parse_line(vcf_file)
                except StopIteration:
                    vcf_end = True
                except ValueError as err:
                    raise ValueError(f"vcf has wrong line: {err}") from None
                try:
                    txt_pos, _ = _parse_line(txt_file)
                except StopIteration:
                    txt_end = True
                except ValueError as err:
                    raise ValueError(f"position file has wrong format: {err}") from None
            elif txt_pos > vcf_pos:
                yield line
                try:
                    vcf_pos, line = _parse_line(vcf_file)
                except StopIteration:
                    vcf_end = True
                except ValueError as err:
                    raise ValueError(f"vcf has wrong line: {err}") from None
            else:  # txt_pos < vcf_pos
                try:
                    txt_pos, _ = _parse_line(txt_file)
                except StopIteration:
                    txt_end = True
                except ValueError as err:
                    raise ValueError(f"position file has wrong format: {err}") from None
            if vcf_end:
                break
            elif txt_end: #and not vcf_end
                yield line
                for line in _until_the_end(vcf_file):
                    yield line
                break

