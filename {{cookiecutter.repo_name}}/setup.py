#!/usr/bin/env python
#
# Copyright 2014 {{cookiecutter.author}}
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/gpl.html>
#
# This module is part of {{cookiecutter.repo_name}}
"""setup tools installer for {{cookiecutter.repo_name}}."""

import os
import sys
from pip.req import parse_requirements
from setuptools import find_packages
from setuptools import setup
from setuptools.command.build_py import build_py

# local imports
try:
    from build_scripts.version import VersionInfo
except:
    pass

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.rst')).read()

version = None
try:
    version = VersionInfo().version
except:
    pass

if version is None:
    try:
        file_name = "{{cookiecutter.repo_name}}/RELEASE-VERSION"
        version_file = open(file_name, "r")
        try:
            version = version_file.readlines()[0]
            version = version.strip()
        except:
            version = "0.0.0"
        finally:
            version_file.close()
    except IOError:
        version = "0.0.0"


class CustomBuild(build_py):

    """custom build class."""

    def run(self):
        """add target and write the release-version file."""
        # honor the --dry-run flag
        if not self.dry_run:
            target_dirs = []
            target_dirs.append(os.path.join(self.build_lib,
                                            '{{cookiecutter.repo_name}}'))
            target_dirs.append('{{cookiecutter.repo_name}}')
            # mkpath is a distutils helper to create directories
            for dir in target_dirs:
                self.mkpath(dir)

            try:
                for dir in target_dirs:
                    fobj = open(os.path.join(dir, 'RELEASE-VERSION'), 'w')
                    fobj.write(version)
                    fobj.close()
            except:
                pass

        super().run()

dev_reqs_gen = parse_requirements("dev-requirements.txt")
dev_requires = [str(ir.req) for ir in dev_reqs_gen]

reqs_gen = parse_requirements("requirements.txt")
install_requires = [str(ir.req) for ir in reqs_gen]

# readline is always here on linux
if not sys.platform.startswith('linux'):
    install_requires.append('readline')

setup(name='{{cookiecutter.repo_name}}',
      version=version,
      description="{{cookiecutter.description}}",
      long_description=README + '\n\n' + NEWS,
      cmdclass={'build_py': CustomBuild},
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.4",
          "Operating System :: Linux", ],
      keywords='{{cookiecutter.keywords}}',
      author='{{cookiecutter.author}}',
      author_email='',
      url='{{cookiecutter.url}}',
      license='LICENSE.txt',
      packages=find_packages(exclude=['ez_setup']),
      package_data={'': ['*.rst', '*.cfg'], },
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=dev_requires,
      install_requires=install_requires,
      entry_points={
          'console_scripts':
          ['='
           '{{cookiecutter.repo_name}}.commands:', ]})
