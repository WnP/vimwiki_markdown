#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="vimwiki-markdown",
    description="vimwiki-markdown: "
    "vimwiki markdown file to html with syntax highlighting.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.4.1",
    py_modules=["vimwiki_markdown"],
    packages=[],
    package_data={},
    license="MIT License",
    author="Steeve Chailloux",
    author_email="github.unrented556" "@" "passmail.net",
    url="https://github.com/WnP/vimwiki_markdown/",
    entry_points={
        "console_scripts": [["vimwiki_markdown = vimwiki_markdown:main"]]
    },
    install_requires=["markdown", "Pygments"],
    extras_require={},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Text Editors",
    ],
)
