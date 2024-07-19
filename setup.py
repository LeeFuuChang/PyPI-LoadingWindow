from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "2.1.0"
DESCRIPTION = "An easy to use LoadingWindow for Apps that needs pre-setups"

# Setting up
setup(
    name="LoadingWindow",
    version=VERSION,
    author="LeeFuuChang",
    author_email="a0962014248gg@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/LeeFuuChang/PyPi-LoadingWindow",
    project_urls={
        # "Documentation": "",
        # "Funding": "",
        "Source": "https://github.com/LeeFuuChang/PyPi-LoadingWindow",
        "Tracker": "https://github.com/LeeFuuChang/PyPi-LoadingWindow/issues",
    },
    packages=find_packages(),
    install_requires=["PyQt5"],
    keywords=["python", "python3", "PyQt5", "Loading Window"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)