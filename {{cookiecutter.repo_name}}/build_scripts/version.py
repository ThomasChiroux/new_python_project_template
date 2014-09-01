"""get version number from dvcs."""
import io
from subprocess import Popen, PIPE


__version__ = "0.0.0"


def get_changelog_rst(outputfile):
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

    def _get_hg_version(self, branch=None):
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
    def current_branch(self):
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

    @property
    def version(self):
        """return the calculed version number."""
        return self._get_hg_version(self.current_branch)


if __name__ == '__main__':
    print(VersionInfo().version)
