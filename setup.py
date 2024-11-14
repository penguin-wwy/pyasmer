import multiprocessing
import os
import subprocess
import sys

import platform
from distutils.extension import Extension
from pathlib import Path

CMAKE_BUILD_TYPE = os.getenv("CMAKE_BUILD_TYPE", "Release")
MAX_JOBS = os.getenv("MAX_JOBS", str(multiprocessing.cpu_count()))

python_min_version = (3, 6, 0)
python_min_version_str = ".".join(map(str, python_min_version))
if sys.version_info < python_min_version:
    print(
        f"You are using Python {platform.python_version()}. Python >={python_min_version_str} is required."
    )
    sys.exit(-1)
version_range_max = max(sys.version_info[1], 10) + 1

import importlib
import importlib.util
import shutil

import setuptools.command.build_ext
from setuptools import setup
from setuptools.dist import Distribution


def _get_package_path(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec:
        # The package might be a namespace package, so get_data may fail
        try:
            loader = spec.loader
            if loader is not None:
                file_path = loader.get_filename()  # type: ignore[attr-defined]
                return os.path.dirname(file_path)
        except AttributeError:
            pass
    return None


CWD = Path(os.path.abspath(__file__))
PROJECT_ROOT = CWD.parent
PYTHON_PACKAGE = PROJECT_ROOT / "pyasmer"


class build_ext(setuptools.command.build_ext.build_ext):
    def build_extensions(self):
        build_fold = Path(self.build_lib) / "build"
        build_fold.mkdir(parents=True, exist_ok=True)
        cmake_config_args = [
            "cmake",
            f"-DCMAKE_BUILD_TYPE={CMAKE_BUILD_TYPE}",
            f"-DPython3_EXECUTABLE={sys.executable}",
            str(PROJECT_ROOT),
        ]
        cmake_build_args = [
            "cmake",
            "--build",
            ".",
            "--config",
            f"{CMAKE_BUILD_TYPE}",
            "--target",
            "_pyasmer",
            f"--",
            f"-j{MAX_JOBS}",
        ]
        try:
            subprocess.check_call(cmake_config_args, cwd=str(build_fold))
            subprocess.check_call(cmake_build_args, cwd=str(build_fold))
        except subprocess.CalledProcessError as e:
            print("cmake build failed with\n", e)
            sys.exit(-1)
        shutil.copy(
            str(build_fold / "_pyasmer.so"), str(PYTHON_PACKAGE / "_pyasmer.so")
        )


class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])


def main():
    install_requires = []

    # Parse the command line and check the arguments before we proceed with
    # building deps and setup. We need to set values so `--help` works.
    dist = Distribution()
    dist.script_name = os.path.basename(sys.argv[0])
    dist.script_args = sys.argv[1:]
    try:
        dist.parse_command_line()
    except Exception as e:
        print(e)
        sys.exit(1)

    package_data = {
        "pyasmer": [
            "_pyasmer.so",
        ],
    }

    with open("README.md", "r") as fp:
        long_desc = "".join(fp.readlines())

    setup(
        name="pyasmer",
        author_email="penguin.wenyang.wang@gmail.com",
        version="0.2.0",
        description="pyasmer",
        long_description=long_desc,
        long_description_content_type="text/markdown",
        url="https://github.com/penguin-wwy/pyasmer",
        author="penguin-wwy",
        python_requires=">=3.6,<3.11",
        # PyPI package information.
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: Implementation :: CPython",
        ]
        + [
            f"Programming Language :: Python :: 3.{i}"
            for i in range(python_min_version[1], version_range_max)
        ],
        license="MIT License",
        packages=["pyasmer"],
        include_package_data=True,
        cmdclass={
            "build_ext": build_ext,
        },
        ext_modules=[CMakeExtension("_pyasmer")],
        install_requires=install_requires,
        package_data=package_data,
    )


if __name__ == "__main__":
    main()
