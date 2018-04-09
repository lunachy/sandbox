# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.common.abstracts import Package


class WPS(Package):
    """Word analysis package."""
    PATHS = [
        ("ProgramFiles", "WPS Office Personal", "office6", "wps.exe"),
    ]

    def start(self, path):
        word = self.get_path("Microsoft Office Word")
        return self.execute(word, "\"%s\" /q" % path, path)
