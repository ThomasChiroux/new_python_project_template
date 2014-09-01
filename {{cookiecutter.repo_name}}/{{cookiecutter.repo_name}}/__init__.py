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
"""determine the module version number."""

import pkg_resources

__version__ = "unknown"

try:
    __version__ = pkg_resources.resource_string(
        "{{cookiecutter.repo_name}}",
        "RELEASE-VERSION").decode('utf-8').strip()
except IOError:
    __version__ = "0.0.0"
