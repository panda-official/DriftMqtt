""" Setup script
"""
import os
from pathlib import Path

from setuptools import setup, find_packages

PACKAGE_NAME = "drift-mqtt"
MAJOR_VERSION = 1
MINOR_VERSION = 0
PATCH_VERSION = 1  # probably will never be used
VERSION_SUFFIX = os.getenv("VERSION_SUFFIX")

HERE = Path(__file__).parent.resolve()


def update_package_version(path: Path, version: str):
    """Overwrite/create __init__.py file and fill __version__"""
    with open(path / "VERSION", "w") as version_file:
        version_file.write(f"{version}\n")


def build_version():
    """Build dynamic version and update version in package"""
    version = f"{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}"
    if VERSION_SUFFIX:
        version += f".{VERSION_SUFFIX}"

    update_package_version(HERE / "pkg" / "drift_mqtt", version=version)

    return version


def get_long_description(base_path: Path):
    """Get long package description"""
    return (base_path / "README.md").read_text(encoding="utf-8")


setup(
    name=PACKAGE_NAME,
    version=build_version(),
    description="Drift MQTT tools",
    long_description=get_long_description(HERE),
    long_description_content_type="text/markdown",
    url="https://gitlab.panda.technology/drift/sdk/drift-mqtt",
    author="PANDA, GmbH",
    author_email="info@panda.technology",
    package_dir={"": "pkg"},
    package_data={"": ["VERSION"]},
    packages=find_packages(where="pkg"),
    python_requires=">=3.7",
    install_requires=["paho-mqtt==1.5.0"],
    extras_require={
        "test": [
            "pytest==6.1.2",
            "lovely-pytest-docker==0.2.0",
            "six==1.15.0",
        ],
        "lint": [
            "pylint==2.5.3",
        ],
    },
)
