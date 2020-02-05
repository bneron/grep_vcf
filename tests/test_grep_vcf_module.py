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

from tests import GrepVcfTest
from io import StringIO

from grep_vcf import grep_vcf


class GrepVcfTestModule(GrepVcfTest):

    def setUp(self) -> None:
        self.pos_text = ["4\tline 1\n",
                         "5\tline 2\n",
                         "# comment 1\n",
                         "#comment 2\n",
                         "8\tline 3\n",
                         "9\tline 4\n",
                         "10\tline 5\n",
                         "11\tline 6\n"]
        self.vcf_text = ["# comment 1\n",
                         "7\tvcf line 1\n",
                         "8\tvcf line 2\n",
                         "9\tvcf line 3\n",
                         "# vcf comment 2\n",
                         "11\tvcf line 4\n",
                         "12\tvcf line 5\n"]

    def test_parse_line(self):
        pos_txt = StringIO(''.join(self.pos_text))
        pos, line = grep_vcf._parse_line(pos_txt)
        self.assertEqual(pos, 4)
        self.assertEqual(line, self.pos_text[0])
        pos, line = grep_vcf._parse_line(pos_txt)
        self.assertEqual(pos, 5)
        self.assertEqual(line, self.pos_text[1])
        pos, line = grep_vcf._parse_line(pos_txt)
        self.assertEqual(pos, 8)
        self.assertEqual(line, self.pos_text[4])

        pos_txt = StringIO("4.5 line 1\n")
        with self.assertRaises(ValueError) as ctx:
            _ = grep_vcf._parse_line(pos_txt)
        self.assertEqual(str(ctx.exception),
                         "4.5 line 1: invalid literal for int() with base 10: '4.5'")

    def test_until_the_end(self):
        pos_txt = StringIO(''.join(self.pos_text))
        lines = [l for l in grep_vcf._until_the_end(pos_txt)]
        expected_lines = [l for l in self.pos_text if l[0] not in ('#', '\n')]
        self.assertListEqual(lines, expected_lines)


    def test_match_generator(self):
        pos_txt = StringIO(''.join(self.pos_text))
        vcf_txt = StringIO(''.join(self.vcf_text))

        diff = list(grep_vcf.match_generator(pos_txt, vcf_txt))
        self.assertListEqual(diff, ["8\tvcf line 2\n",
                                    "9\tvcf line 3\n",
                                    "11\tvcf line 4\n"
                                    ])

    def test_match_generator_bad_pos1(self):
        vcf_txt = StringIO(''.join(self.vcf_text))
        pos_text = self.pos_text[:]
        pos_text.insert(0, "3.5\tbad position\n")
        pos_txt = StringIO(''.join(pos_text))

        with self.assertRaises(ValueError):
            _ = list(grep_vcf.match_generator(pos_txt, vcf_txt))

    def test_match_generator_bad_pos2(self):
        vcf_txt = StringIO(''.join(self.vcf_text))
        pos_text = self.pos_text[:]
        pos_text.insert(1, "4.5\tbad position\n")
        pos_txt = StringIO(''.join(pos_text))

        with self.assertRaises(ValueError):
            _ = list(grep_vcf.match_generator(pos_txt, vcf_txt))

    def test_match_generator_bad_pos3(self):
        vcf_txt = StringIO(''.join(self.vcf_text))
        pos_text = self.pos_text[:]
        pos_text.insert(4, "8.5\tbad position\n")
        pos_txt = StringIO(''.join(pos_text))

        with self.assertRaises(ValueError):
            _ = list(grep_vcf.match_generator(pos_txt, vcf_txt))

    def test_match_generator_bad_pos4(self):
        vcf_txt = StringIO(''.join(self.vcf_text))
        pos_text = self.pos_text[:]
        pos_text.insert(5, "8.5\tbad position\n")
        pos_txt = StringIO(''.join(pos_text))

        with self.assertRaises(ValueError):
            _ = list(grep_vcf.match_generator(pos_txt, vcf_txt))


    def test_match_generator_bad_vcf1(self):
        pos_txt = StringIO(''.join(self.pos_text))
        vcf_text = self.vcf_text[:]
        vcf_text.insert(0, "3.5\tbad vcf\n")
        vcf_txt = StringIO(''.join(vcf_text))

        with self.assertRaises(ValueError):
            _ = list(grep_vcf.match_generator(pos_txt, vcf_txt))

    def test_match_generator_bad_vcf2(self):
        pos_txt = StringIO(''.join(self.pos_text))
        vcf_text = self.vcf_text[:]
        vcf_text.insert(2, "7.5\tbad vcf\n")
        vcf_txt = StringIO(''.join(vcf_text))

        with self.assertRaises(ValueError):
            _ = list(grep_vcf.match_generator(pos_txt, vcf_txt))

    def test_match_generator_bad_vcf3(self):
        pos_txt = StringIO(''.join(self.pos_text))
        vcf_text = self.vcf_text[:]
        vcf_text.insert(3, "8.5\tbad position\n")
        vcf_txt = StringIO(''.join(vcf_text))

        with self.assertRaises(ValueError):
            _ = list(grep_vcf.match_generator(pos_txt, vcf_txt))

    def test_match_generator_empty(self):
        pos_txt = StringIO('')
        vcf_txt = StringIO('')
        diff = list(grep_vcf.match_generator(pos_txt, vcf_txt))
        self.assertListEqual(diff, [])

    def test_match_generator_pos_empty(self):
        pos_txt = StringIO('')
        vcf_txt = StringIO(''.join(self.vcf_text))
        diff = list(grep_vcf.match_generator(pos_txt, vcf_txt))
        self.assertListEqual(diff, [])

    def test_match_generator_vcf_empty(self):
        pos_txt = StringIO(''.join(self.pos_text[:]))
        vcf_txt = StringIO('')
        diff = list(grep_vcf.match_generator(pos_txt, vcf_txt))
        self.assertListEqual(diff, [])


    def test_invert_match_generator(self):
        pos_txt = StringIO(''.join(self.pos_text))
        vcf_txt = StringIO(''.join(self.vcf_text))
        diff = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))
        self.assertListEqual(diff, ["7\tvcf line 1\n",
                                    "12\tvcf line 5\n",
                                    ])

    def test_invert_match_generator_bad_pos1(self):
        pos_text = self.pos_text[:]
        pos_text.insert(0, "3.5 bad position")
        pos_txt = StringIO(''.join(pos_text))
        vcf_txt = StringIO(''.join(self.vcf_text))
        with self.assertRaises(ValueError):
            _ = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))

    def test_match_generator_bad_pos2(self):
        vcf_txt = StringIO(''.join(self.vcf_text))
        pos_text = self.pos_text[:]
        pos_text.insert(1, "4.5\tbad position\n")
        pos_txt = StringIO(''.join(pos_text))

        with self.assertRaises(ValueError):
            _ = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))

    def test_invert_match_generator_bad_pos3(self):
        vcf_txt = StringIO(''.join(self.vcf_text))
        pos_text = self.pos_text[:]
        pos_text.insert(5, "8.5\tbad position\n")
        pos_txt = StringIO(''.join(pos_text))

        with self.assertRaises(ValueError):
            _ = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))

    def test_invert_match_generator_bad_vcf1(self):
        pos_txt = StringIO(''.join(self.pos_text))
        vcf_text = self.vcf_text[:]
        vcf_text.insert(0, "3.5\tbad vcf\n")
        vcf_txt = StringIO(''.join(vcf_text))

        with self.assertRaises(ValueError):
            _ = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))

    def test_invert_match_generator_bad_vcf2(self):
        pos_txt = StringIO(''.join(self.pos_text))
        vcf_text = self.vcf_text[:]
        vcf_text.insert(2, "7.5\tbad vcf\n")
        vcf_txt = StringIO(''.join(vcf_text))

        with self.assertRaises(ValueError):
            _ = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))

    def test_invert_match_generator_bad_vcf3(self):
        pos_txt = StringIO(''.join(self.pos_text))
        vcf_text = self.vcf_text[:]
        vcf_text.insert(3, "8.5\tbad position\n")
        vcf_txt = StringIO(''.join(vcf_text))

        with self.assertRaises(ValueError):
            _ = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))

    def test_invert_match_empty_pos(self):
        pos_txt = StringIO('')
        vcf_txt = StringIO(''.join(self.vcf_text))
        diff = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))
        expected_lines = [l for l in self.vcf_text if l[0] not in ('#', '\n')]
        self.assertListEqual(diff, expected_lines)

    def test_invert_match_empty(self):
        pos_txt = StringIO('')
        vcf_txt = StringIO('')
        diff = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))
        self.assertListEqual(diff, [])

    def test_invert_match_empty_vcf(self):
        pos_txt = StringIO(''.join(self.pos_text[:]))
        vcf_txt = StringIO('')
        diff = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))
        self.assertListEqual(diff, [])

    def test_invert_match_trunked_vcf(self):
        # vcf == pos and vcf file is shorter than pos file
        pos_txt = StringIO('8\tline 1\n9\tline 2\n')
        vcf_txt = StringIO('8\tvcf 1\n')
        diff = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))
        self.assertListEqual(diff, [])

    def test_invert_match_trunked_vcf2(self):
        # vcf < pos and vcf file is shorter than pos file
        pos_txt = StringIO('9\tline 1\n10\tline 2\n')
        vcf_txt = StringIO('8\tvcf 1\n')
        diff = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))
        self.assertListEqual(diff, ['8\tvcf 1\n'])

    def test_invert_match_trunked_pos(self):
        # pos == vcf and pos file is shorter than vcf file
        pos_txt = StringIO('9\tline 1\n')
        vcf_txt = StringIO('9\tvcf 1\n10\tvcf 2\n11\tvcf 3\n')
        diff = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))
        self.assertListEqual(diff, ['10\tvcf 2\n', '11\tvcf 3\n'])

    def test_invert_match_trunked_pos(self):
        # pos < vcf and pos file is shorter than vcf file
        pos_txt = StringIO('7\tline 1\n')
        vcf_txt = StringIO('9\tvcf 1\n10\tvcf 2\n11\tvcf 3\n')
        diff = list(grep_vcf.invert_match_generator(pos_txt, vcf_txt))
        self.assertListEqual(diff, ['9\tvcf 1\n',
                                    '10\tvcf 2\n',
                                    '11\tvcf 3\n'])