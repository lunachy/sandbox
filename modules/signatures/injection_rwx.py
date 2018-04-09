# Copyright (C) 2014 Accuvant, Inc. (bspengler@accuvant.com)
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class InjectionRWX(Signature):
    name = "injection_rwx"
    description = "Creates RWX memory"
    severity = 2
    confidence = 50
    categories = ["injection"]
    authors = ["Accuvant"]
    minimum = "1.2"
    evented = True

    def __init__(self, *args, **kwargs):
        Signature.__init__(self, *args, **kwargs)
        self.handles = dict()
        self.lastprocess = 0
        self.stealth_files = []
        self.is_office = False
        office_pkgs = ["docx","ppt","doc","xls","eml","pptx","xlsx"]
        if any(e in self.results["target"]["file"]["name"] for e in office_pkgs):
            self.is_office = True


    filter_apinames = set(["NtAllocateVirtualMemory","NtProtectVirtualMemory","VirtualProtectEx"])
    filter_analysistypes = set(["file"])

    def on_call(self, call, process):
        if self.is_office:
            return False
        else:
            if call["api"] == "NtAllocateVirtualMemory" or call["api"] == "VirtualProtectEx":
                protection = self.get_argument(call, "Protection")
                # PAGE_EXECUTE_READWRITE
                if protection == "0x00000040":
                    return True
            elif call["api"] == "NtProtectVirtualMemory":
                protection = self.get_argument(call, "NewAccessProtection")
                # PAGE_EXECUTE_READWRITE
                if protection == "0x00000040":
                    return True

        
