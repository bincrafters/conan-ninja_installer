from conans import ConanFile, tools
import os


class NinjaConan(ConanFile):
    name = "ninja"
    version = "1.8.2"
    license = "Apache 2.0"
    description = "Ninja is a small build system with a focus on speed"
    url = "https://github.com/SSE4/conan-ninja_installer"
    no_copy_source = True
    settings = {"os"}
    repository = "https://chromium.googlesource.com/chromium/tools/depot_tools.git"

    def source(self):
        if self.settings.os == "Windows":
            platform = "win"
        elif self.settings.os == "Linux":
            platform = "linux"
        elif self.settings.os == "Macos" or self.settings.os == "iOS":
            platform = "mac"
        else:
            raise Exception("unsupported os %s" % self.settings.os)

        archive_name = "ninja-%s.zip" % platform
        url = "https://github.com/ninja-build/ninja/releases/download/v%s/%s" % (self.version, archive_name)
        tools.download(url, archive_name, verify=True)
        tools.unzip(archive_name)
        os.unlink(archive_name)

    def package(self):
        if self.settings.os == "Windows":
            self.copy(pattern="ninja.exe", dst=".", src=".")
        else:
            self.copy(pattern="ninja", dst=".", src=".")

    def package_info(self):
        bin_path = os.path.join(self.package_folder)
        self.env_info.path.append(bin_path)
