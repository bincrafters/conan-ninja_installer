#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class NinjaConan(ConanFile):
    name = "ninja_installer"
    version = "1.8.2"
    license = "Apache 2.0"
    export = ["LICENSE.md"]
    description = "Ninja is a small build system with a focus on speed"
    url = "https://github.com/bincrafters/conan-ninja_installer"
    settings = {'os_build': ['Windows', 'Linux', 'Macos'], 'arch_build': ['x86', 'x86_64'], 'compiler': None}

    def requirements(self):
        if self.settings.os_build == 'Linux':
            self.requires.add('glibc_version_header/0.1@bincrafters/stable')

    def build_vs(self):
        with tools.chdir('sources'):
            with tools.vcvars(self.settings, filter_known_paths=False):
                self.run('python configure.py --bootstrap')

    def build_configure(self):
        with tools.chdir('sources'):
            cxx = os.environ.get('CXX', 'g++')
            if self.settings.arch_build == 'x86':
                cxx += ' -m32'
            elif self.settings.arch_build == 'x86_64':
                cxx += ' -m64'
            os.environ['CXX'] = cxx
            env_build = AutoToolsBuildEnvironment(self)
            with tools.environment_append(env_build.vars):
                self.run('./configure.py --bootstrap')

    def source(self):
        archive_name = "v%s.tar.gz" % self.version
        url = "https://github.com/ninja-build/ninja/archive/%s" % archive_name
        tools.get(url)
        os.rename('ninja-%s' % self.version, 'sources')

    def build(self):
        if self.settings.os_build == 'Windows':
            self.build_vs()
        else:
            self.build_configure()

    def package(self):
        self.copy(pattern="ninja*", dst='bin', src='sources')

    def package_info(self):
        # ensure ninja is executable
        if str(self.settings.os_build) in ['Linux', 'Macosx']:
            name = os.path.join(self.package_folder, 'bin', 'ninja')
            os.chmod(name, os.stat(name).st_mode | 0o111)
        self.env_info.PATH.append(os.path.join(self.package_folder, 'bin'))
        self.env_info.CONAN_CMAKE_GENERATOR = 'Ninja'

    def package_id(self):
        self.info.settings.compiler = 'Any'
