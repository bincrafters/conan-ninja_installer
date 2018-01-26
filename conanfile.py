#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class NinjaConan(ConanFile):
    name = "ninja_installer"
    version = "1.8.2"
    license = "Apache 2.0"
    export = ["LICENSE.md"]
    description = "Ninja is a small build system with a focus on speed"
    url = "https://github.com/SSE4/conan-ninja_installer"
    no_copy_source = True
    settings = 'os_build'

    def build(self):
        platform_name = {"Windows": "win", "Linux": "linux", "Macosx": "mac"}.get(str(self.settings.os_build))
        archive_name = "ninja-%s.zip" % platform_name
        url = "https://github.com/ninja-build/ninja/releases/download/v%s/%s" % (self.version, archive_name)
        tools.download(url, archive_name, verify=True)
        tools.unzip(archive_name)
        os.unlink(archive_name)

    def package(self):
        self.copy(pattern="ninja*", dst='bin', src='.')

    def package_info(self):
        # ensure ninja is executable
        if str(self.settings.os_build) in ['Linux', 'Macosx']:
            name = 'ninja'
            os.chmod(name, os.stat(name).st_mode | 0o111)
        self.env_info.PATH.append(os.path.join(self.package_folder, 'bin'))
