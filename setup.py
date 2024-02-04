#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from os import path
from pathlib import Path  # noqa

from setuptools import find_packages, setup

HERE = path.abspath(path.dirname(__file__))
root_module = "zivijo"


class About:
	"""About class."""

	@staticmethod
    def add_default(match):
		"""add_default."""
        attr_name, attr_value = match.groups()
        return (attr_name, attr_value.strip("\"'")),

    def info(self) -> dict:
        content = {}

        re_meta = re.compile(r"^__(\w+?)__\s*=\s*(.*)")
        parts = {re_meta: self.add_default}

        version_file = path.join(HERE, f"src/{root_module}", "__version__.py")
        with open(version_file, encoding="utf-8") as f_obj:
            for line in f_obj:
                for pattern, handler in parts.items():
                    m = pattern.match(line.strip())
                    if m:
                        content.update(handler(m))
        return content


# Preparation
about = About().info()
with open("requirements.txt", "r") as requirements:
    install_requires = [
        str(requirement)
        for requirement
        in requirements.readlines()
        if not requirement.startswith("#") or not requirement.startswith("--")
    ]

# Run SETUP
setup(
    name=about["title"],
    description=about["description"],
    long_description=open("README.md").read().rstrip(),
    long_description_content_type="text/markdown",
    license=about["license"],
    url=about["url"],
    version=about["version"],
    author=about["author"],
    author_email=about["author_email"],
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    classifiers=["Programming Language :: Python :: 3.9",
                 "Programming Language :: Python :: 3.10"],
    python_requires=">=3.9, <=3.10",
    # It is better to list the requirements and not to mix the purpose of requirements.txt with the install_requires
    install_requires=install_requires
)
