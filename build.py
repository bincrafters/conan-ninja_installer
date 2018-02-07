#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default

if __name__ == "__main__":

    filtered_builds = []
    builder = build_template_default.get_builder()
    for settings, options, env_vars, build_requires, reference in builder.items:
        settings["arch_build"] = settings["arch"]
        del settings["arch"]
    filtered_builds.append([settings, options, env_vars, build_requires])
    builder.builds = filtered_builds
    builder.run()
