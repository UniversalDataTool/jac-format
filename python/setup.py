from os.path import join, abspath, dirname
from setuptools import setup, find_packages

_here = abspath(dirname(__file__))


with open(join(_here, "README.md")) as f:
    readme = f.read()

with open(join(_here, "LICENSE")) as f:
    license = f.read().replace("\n", "")

setup(
    name="jac_format",
    version="0.1.1",
    description="JAC (JSON as CSV) Format Conversion",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="UniversalDataTool",
    author_email="seve@wao.ai",
    url="https://github.com/UniversalDataTool/jac-format",
    license=license,
    packages=["jac_format"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ],
)
