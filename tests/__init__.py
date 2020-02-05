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
# along with grep_vcf (LICENSE).                                     #
# If not, see <https://www.gnu.org/licenses/>.                          #
#########################################################################

import unittest
import os


class GrepVcfTest(unittest.TestCase):

    _tests_dir = os.path.normpath(os.path.dirname(__file__))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    @classmethod
    def find_data(cls, *args):
        data_path = os.path.join(cls._data_dir, *args)
        if os.path.exists(data_path):
            return data_path
        else:
            raise IOError("data '{}' does not exists".format(data_path))
