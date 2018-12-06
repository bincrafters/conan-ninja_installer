#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment


class NinjaConan(ConanFile):
    name = "ninja_installer"
    version = "1.8.2_kitware"
    description = "Ninja is a small build system with a focus on speed"
    license = "Apache-2.0"
    url = "https://github.com/bincrafters/conan-ninja_installer"
    homepage = "https://github.com/ninja-build/ninja"
    author = "Bincrafters <bincrafters@gmail.com>"
    export = ["LICENSE.md"]
    settings = {
        "os_build": ["Windows", "Linux", "Macos"],
        "arch_build": ["x86", "x86_64"],
        "compiler": None
    }
    _source_subfolder = "source_subfolder"

    def _build_vs(self):
        with tools.chdir(self._source_subfolder):
            with tools.vcvars(self.settings, filter_known_paths=False):
                self.run("python configure.py --bootstrap")

    def _build_configure(self):
        with tools.chdir(self._source_subfolder):
            cxx = os.environ.get("CXX", "g++")
            if self.settings.os_build == "Linux":
                if self.settings.arch_build == "x86":
                    cxx += " -m32"
                elif self.settings.arch_build == "x86_64":
                    cxx += " -m64"
            os.environ["CXX"] = cxx
            env_build = AutoToolsBuildEnvironment(self)
            with tools.environment_append(env_build.vars):
                self.run("python configure.py --bootstrap")

    def source(self):
        # intentionally not using source method to avoid caching
        tag = "1.8.2.g81279.kitware.dyndep-1.jobserver-1"
        url = "https://github.com/Kitware/ninja"
        archive_name = "v%s.tar.gz" % tag
        tools.get("%s/archive/%s" % (url, archive_name))
        os.rename("ninja-%s" % tag, self._source_subfolder)

    def build(self):
        if self.settings.os_build == "Windows":
            self._build_vs()
        else:
            self._build_configure()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="ninja*", dst="bin", src=self._source_subfolder)

    def package_info(self):
        # ensure ninja is executable
        if str(self.settings.os_build) in ["Linux", "Macosx"]:
            name = os.path.join(self.package_folder, "bin", "ninja")
            os.chmod(name, os.stat(name).st_mode | 0o111)
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.CONAN_CMAKE_GENERATOR = "Ninja"

    def package_id(self):
        self.info.settings.compiler = "Any"
