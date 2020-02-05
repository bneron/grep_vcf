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

from setuptools import setup, find_packages
from setuptools.dist import Distribution

from grep_vcf import __version__ as gv_version


class UsageDistribution(Distribution):

    def __init__(self, attrs=None):
        # It's important to define options before to call __init__
        # otherwise AttributeError: UsageDistribution instance has no attribute 'conf_files'
        self.fix_prefix = None
        Distribution.__init__(self, attrs=attrs)
        self.common_usage = """\
Common commands: (see '--help-commands' for more)

  setup.py build      will build the package underneath 'build/'
  setup.py install    will install the package
  setup.py test       run tests after in-place build
"""


###################################################
# the configuration of the installer start bellow #
###################################################

setup(name='grep_vcf',
      version=gv_version,
      description="",
      long_description='README.md',
      author="Bertrand Néron",
      author_email="bneron@pasteur.fr",
      url="https://github.com/bneron/grep_vcf",
      download_url='https://github.com/bneron/grep_vcf',
      license="GPLv3",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics'
          ],
      python_requires='>=3.6',
      extras_require={'dev': open("requirements_dev.txt").read().split()},
      test_suite='tests.run_tests.discover',
      packages=[p for p in find_packages() if p != 'tests'],
      entry_points={
          'console_scripts': [
              'grep_vcf=grep_vcf.scripts.grep_vcf:main',
          ]
      },
      distclass=UsageDistribution
      )
