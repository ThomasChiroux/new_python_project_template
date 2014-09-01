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
"""get version number from dvcs.

works for either git or mercurial repo.
"""
import io
from subprocess import Popen, PIPE


__version__ = "0.0.0"


def hg_get_changelog_rst(outputfile):
    """output a rst file with the change log in compact version."""
    p = Popen([
        "hg", "log",
        "--style", "build_scripts/hg_changelog.style"],
        stdout=PIPE, stderr=PIPE)
    p.stderr.close()
    fp = io.open(outputfile, "w", encoding='utf-8')
    fp.write(u'=========\n')
    fp.write(u'Changelog\n')
    fp.write(u'=========\n\n')
    for line in iter(p.stdout.readline, b''):  # block / wait
        fp.write(line.decode('utf-8'))

    fp.close()


class VersionInfo():

    """object that get version information from dvcs."""

    stable_branch = "stable"

    def _popen(self, command_list):
        """launch subprocess for given command.

        return a list of (returned) lines
        """
        try:
            p = Popen(command_list,
                      stdout=PIPE, stderr=PIPE)
            p.stderr.close()
            lines = p.stdout.readlines()
            return lines
        except Exception:
            return []

    def read_release_version(self):
        """try to read the release version file."""
        try:
            f = open("RELEASE-VERSION", "r")

            try:
                version = f.readlines()[0]
                return version.strip()

            finally:
                f.close()
        except:
            return None

    def write_release_version(self, version):
        """write the release version file."""
        f = open("RELEASE-VERSION", "w")
        f.write("%s\n" % version)
        f.close()

    def _is_git_repo(self):
        """try to detect if the repo is a git repo."""
        if self._popen(["git", "status"]):
            return True
        else:
            return False

    def _is_hg_repo(self):
        """try to detect if the repo is a git repo."""
        if self._popen(["hg", "status"]):
            return True
        else:
            return False

    def _hg_get_version(self, branch=None):
        """use mercurial to get last tag and last revision number.

        if repo has just been tagged, return 'lasttag'
        if not, return 'lasttag-lastrevnum'
        """
        cmd_hg_log = ["hg", "log", "--limit", "1",
                      "--template", "{latesttag};{rev}"]
        if branch is not None and branch:
            cmd_hg_log += ["-b", branch]

        line = self._popen(cmd_hg_log)[0].decode('utf-8')
        try:
            latest_tag, latest_rev = line.strip().split(';')
        except ValueError:
            return ""
        else:
            cmd_hg_log_rev = ["hg", "log",  # "--limit", "1",
                              "-r", '"%s"' % latest_tag,
                              "--template", "{rev}"]

            line = self._popen(cmd_hg_log_rev)[0].decode('utf-8')
            latest_tag_rev = line.strip()

            if int(latest_tag_rev) == int(latest_rev) - 1:
                # here our version has just been tagged,
                # return only version number
                return latest_tag
            else:
                # we have commits since last tag
                # the return value will depends on the current branch:
                # if in stable branch, tag ".postXXXX"
                # otherwise (in dev branches), tag '.devXXXXX'
                if branch is not None and branch == self.stable_branch:
                    return "%s.post%s" % (latest_tag, latest_rev)
                else:
                    return "%s.dev%s" % (latest_tag, latest_rev)

    @property
    def _hg_current_branch(self):
        """use mercurial to get the current branch.

        In case of problem, returns empty string
        """
        try:
            p = Popen(["hg", "branch"],
                      stdout=PIPE, stderr=PIPE)
            p.stderr.close()
            line = p.stdout.readlines()[0].decode('utf-8')
            return line.strip()
        except Exception:
            return ''

    def _git_call_describe(self, abbrev=4):
        try:
            p = Popen(['git', 'describe', '--abbrev=%d' % abbrev],
                      stdout=PIPE, stderr=PIPE)
            p.stderr.close()
            line = p.stdout.readlines()[0]
            return line.strip()

        except:
            return None

    def _git_get_version(self, abbrev=4):
        # Read in the version that's currently in RELEASE-VERSION.

        release_version = self.read_release_version()

        # First try to get the current version using “git describe”.
        version = self._git_call_describe(abbrev)

        # If that doesn't work, fall back on the value that's in
        # RELEASE-VERSION.

        if version is None:
            version = release_version

        # If we still don't have anything, that's an error.

        if version is None:
            raise ValueError("Cannot find the version number!")

        # If the current version is different from what's in the
        # RELEASE-VERSION file, update the file to be current.

        if version != release_version:
            self.write_release_version(version)

        # Finally, return the current version.
        return version

    @property
    def version(self):
        """return the calculed version number.

        return None if no repo found (git or hg)
        :rtype: str
        """
        if self._is_hg_repo():
            return self._hg_get_version(
                self._hg_current_branch).decode('utf-8')

        if self._is_git_repo():
            return self._git_get_version().decode('utf-8')

if __name__ == '__main__':
    print(VersionInfo().version)
