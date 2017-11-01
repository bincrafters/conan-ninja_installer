from conans import ConanFile, tools
import os
import platform
import stat


class NinjaConan(ConanFile):
    name = "ninja_installer"
    version = "1.8.2"
    license = "Apache 2.0"
    description = "Ninja is a small build system with a focus on speed"
    url = "https://github.com/SSE4/conan-ninja_installer"
    no_copy_source = True

    def build(self):
        for _platform in ["win", "linux", "mac"]:
            os.makedirs(_platform)
            with tools.chdir(_platform):
                archive_name = "ninja-%s.zip" % _platform
                url = "https://github.com/ninja-build/ninja/releases/download/v%s/%s" % (self.version, archive_name)
                tools.download(url, archive_name, verify=True)
                tools.unzip(archive_name)
                os.unlink(archive_name)

    def package(self):
        for _platform in ["win", "linux", "mac"]:
            self.copy(pattern="ninja*", dst=_platform, src=_platform)

    def package_info(self):
        _platform = {'Darwin': 'mac', 'Linux': 'linux', 'Windows': 'win'}.get(platform.system())
        bin_path = os.path.join(self.package_folder, _platform)
        # ensure ninja is executable
        if os.name == 'posix':
            name = os.path.join(bin_path, 'ninja')
            mode = os.stat(name).st_mode
            mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            os.chmod(name, stat.S_IMODE(mode))
        self.env_info.path.append(bin_path)
