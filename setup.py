import setuptools
from clibato import Clibato

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.read().splitlines()

GITHUB_URL = "https://github.com/jigarius/clibato"
AUTHOR_URL = "https://jigarius.com/"

setuptools.setup(
    name="clibato",
    version=Clibato.VERSION,
    author="Jigar Mehta",
    author_email="hello@jigarius.com",
    description="A tool to backup/restore simple files, e.g. dot files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GNU LGPL v2.1',
    url=GITHUB_URL,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    keywords='cli backup restore dotfile utility',
    project_urls={
        "Documentation": GITHUB_URL + '#readme',
        "Author": AUTHOR_URL,
        "Tracker": "https://github.com/jigarius/clibato/issues"
    },
    packages=setuptools.find_packages(exclude=['test']),
    python_requires='>=3.5',
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['clibato=clibato.__main__:main'],
    }
)
