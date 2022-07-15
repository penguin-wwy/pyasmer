from pathlib import Path

from setuptools import Extension
from setuptools import setup

ROOT_PATH = Path(__file__).parent

PYASMER_EXTENSION = Extension(
    name="pyasmer._pyasmer",
    sources=[
        "src/pyasmer.c",
    ],
    libraries=[],
    library_dirs=[],
    include_dirs=["src"],
    language="c",
    extra_compile_args=[],
    extra_link_args=[],
    define_macros=[],
    undef_macros=[],
)

setup(
    name="pyasmer",
    version="0.1",
    python_requires=">=3.10.0",
    description="pyasmer",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/penguin-wwy/pyasmer",
    author="penguin-wwy",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    license="MIT License",
    packages=["pyasmer"],
    ext_modules=[PYASMER_EXTENSION],
    include_package_data=True,
    install_requires=[],
    extras_require={},
)
