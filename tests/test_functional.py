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
import tempfile
import shutil
import os
import sys
from grep_vcf.scripts.grep_vcf import main
from tests import GrepVcfTest


class Functional(GrepVcfTest):

    def test_grep_vcf(self):
        with tempfile.TemporaryDirectory(prefix='test_grep_vcf') as tmpdir:
            pos_file_name = self.find_data('data.txt')
            pos_file_name = shutil.copyfile(pos_file_name,
                                            os.path.join(tmpdir, os.path.basename(pos_file_name)))
            data_file_name = self.find_data('data.vcf')
            data_file_name = shutil.copyfile(data_file_name,
                                             os.path.join(tmpdir, os.path.basename(data_file_name)))
            command = f"grep_vcf {pos_file_name}"
            with self.catch_io(out=True):
                main(args=command.split()[1:])
                stdout = sys.stdout.getvalue().strip()
            self.assertEqual(stdout,
                             "7\tvcf ligne 1\n9\tvcf ligne 3\n11\tvcf ligne 4")

    def test_specify_vcf(self):
        with tempfile.TemporaryDirectory(prefix='test_grep_vcf') as tmpdir:
            pos_file_name = self.find_data('data.txt')
            pos_file_name = shutil.copyfile(pos_file_name,
                                            os.path.join(tmpdir, os.path.basename(pos_file_name)))
            data_file_name = self.find_data('data.vcf')
            data_file_name = shutil.copyfile(data_file_name,
                                             os.path.join(tmpdir, os.path.basename(data_file_name)))
            command = f"grep_vcf --vcf {data_file_name} {pos_file_name}"
            with self.catch_io(out=True):
                main(args=command.split()[1:])
                stdout = sys.stdout.getvalue().strip()
            self.assertEqual(stdout,
                             "7\tvcf ligne 1\n9\tvcf ligne 3\n11\tvcf ligne 4")

    def test_empty_vcf(self):
        with tempfile.TemporaryDirectory(prefix='test_grep_vcf') as tmpdir:
            pos_file_name = self.find_data('data.txt')
            pos_file_name = shutil.copyfile(pos_file_name,
                                            os.path.join(tmpdir, os.path.basename(pos_file_name)))
            data_file_name = self.find_data('empty.vcf')
            data_file_name = shutil.copyfile(data_file_name,
                                             os.path.join(tmpdir, os.path.basename(data_file_name)))
            command = f"grep_vcf --vcf {data_file_name} {pos_file_name}"
            with self.catch_io(out=True):
                main(args=command.split()[1:])
                stdout = sys.stdout.getvalue().strip()
            self.assertEqual(stdout, '')

    def test_empty_positions(self):
        with tempfile.TemporaryDirectory(prefix='test_grep_vcf') as tmpdir:
            pos_file_name = self.find_data('empty.txt')
            pos_file_name = shutil.copyfile(pos_file_name,
                                            os.path.join(tmpdir, os.path.basename(pos_file_name)))
            data_file_name = self.find_data('data.vcf')
            data_file_name = shutil.copyfile(data_file_name,
                                             os.path.join(tmpdir, os.path.basename(data_file_name)))
            command = f"grep_vcf --vcf {data_file_name} {pos_file_name}"
            with self.catch_io(out=True):
                main(args=command.split()[1:])
                stdout = sys.stdout.getvalue().strip()
            self.assertEqual(stdout, '')

    def test_invert(self):
        with tempfile.TemporaryDirectory(prefix='test_grep_vcf') as tmpdir:
            pos_file_name = self.find_data('data.txt')
            pos_file_name = shutil.copyfile(pos_file_name,
                                            os.path.join(tmpdir, os.path.basename(pos_file_name)))
            data_file_name = self.find_data('data.vcf')
            data_file_name = shutil.copyfile(data_file_name,
                                             os.path.join(tmpdir, os.path.basename(data_file_name)))
            command = f"grep_vcf --invert {pos_file_name}"
            with self.catch_io(out=True):
                main(args=command.split()[1:])
                stdout = sys.stdout.getvalue().strip()
            self.assertEqual(stdout,
                             "8\tvcf ligne 2\n12\tvcf ligne 5")

    def test_switch(self):
        with tempfile.TemporaryDirectory(prefix='test_grep_vcf') as tmpdir:
            pos_file_name = self.find_data('data.txt')
            pos_file_name = shutil.copyfile(pos_file_name,
                                            os.path.join(tmpdir, os.path.basename(pos_file_name)))
            data_file_name = self.find_data('data.vcf')
            data_file_name = shutil.copyfile(data_file_name,
                                             os.path.join(tmpdir, os.path.basename(data_file_name)))
            command = f"grep_vcf --switch {pos_file_name}"
            with self.catch_io(out=True):
                main(args=command.split()[1:])
                stdout = sys.stdout.getvalue().strip()
            self.assertEqual(stdout,
                             "7\ttxt ligne 3\n9\ttxt ligne 4\n11\ttxt ligne 6")

    def test_specify_out(self):
        with tempfile.TemporaryDirectory(prefix='test_grep_vcf') as tmpdir:
            pos_file_name = self.find_data('data.txt')
            pos_file_name = shutil.copyfile(pos_file_name,
                                            os.path.join(tmpdir, os.path.basename(pos_file_name)))
            data_file_name = self.find_data('data.vcf')
            data_file_name = shutil.copyfile(data_file_name,
                                             os.path.join(tmpdir, os.path.basename(data_file_name)))
            out_file_name = os.path.join(tmpdir, 'diff.vcf')
            command = f"grep_vcf --out {out_file_name} {pos_file_name}"
            main(args=command.split()[1:])
            with open(out_file_name) as out:
                res = out.read()
            self.assertEqual(res,
                             "7\tvcf ligne 1\n9\tvcf ligne 3\n11\tvcf ligne 4\n")

    def test_no_position_file(self):
        with tempfile.TemporaryDirectory(prefix='test_grep_vcf') as tmpdir:
            pos_file_name = self.find_data('data.txt')
            pos_file_name = os.path.join(tmpdir, os.path.basename(pos_file_name))
            data_file_name = self.find_data('data.vcf')
            data_file_name = shutil.copyfile(data_file_name,
                                             os.path.join(tmpdir, os.path.basename(data_file_name)))
            command = f"grep_vcf {pos_file_name}"
            with self.assertRaises(FileNotFoundError) as ctx:
                main(args=command.split()[1:])
            self.assertEqual(str(ctx.exception),
                             f"The file {pos_file_name} does not exists.")
