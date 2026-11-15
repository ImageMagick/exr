#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Tools"))

from dependency_updater import Step, Updater

URL = "https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/v{version}.tar.gz"

GENERATED_HEADERS = (
    "IexConfig.h",
    "IexConfigInternal.h",
    "IlmThreadConfig.h",
    "OpenEXRConfig.h",
    "OpenEXRConfigInternal.h",
)


def update_source(updater):
    updater.replace_source()
    updater.remove(".github", "external/OpenJPH", "external/zstd")
    updater.apply_patches()
    updater.update_config()


def create_headers(updater):
    updater.cmake(allow_errors=True)
    updater.copy_from_build("cmake", GENERATED_HEADERS)
    updater.remove_build()


updater = Updater(__file__, "openexr", URL)
updater.run([
    Step("Replace the source with the release and update Config.txt", update_source,
        "Updated openexr to {version}"),
    Step("Use cmake to create the header files", create_headers,
        "Use cmake to create the header files."),
    updater.clone_dependencies_step(),
])
