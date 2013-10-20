# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os, sys

version = '0.1.5'
long_description = '\n'.join([
        open(os.path.join("src", "README.txt")).read(),
        open(os.path.join("src", "AUTHORS.txt")).read(),
        open(os.path.join("src", "HISTORY.txt")).read(),
        ])

classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Topic :: Software Development",
    "Topic :: Software Development :: Documentation",
    "Topic :: Text Processing :: Markup",
]

setup(
    name='sphinxjp.themes.bizstyle',
    version=version,
    description='A sphinx theme for Business style Documentation.',
    long_description=long_description,
    classifiers=classifiers,
    keywords=['sphinx', 'reStructuredText', 'theme'],
    author='Shoji KUMAGAI',
    author_email='take dot this dot 2 dot your dot grave at gmail dot com',
    url='https://bitbucket.org/shkumagai/sphinxjp.themes.bizstyle',
    license='MIT',
    namespace_packages=['sphinxjp', 'sphinxjp.themes'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['buildout.cfg']},
    include_package_data=True,
    install_requires=[
        'setuptools',
        'docutils',
        'sphinx',
        'sphinxjp.themecore',
    ],
    entry_points="""
        [sphinx_themes]
        path = sphinxjp.themes.bizstyle:template_path

    """,
    zip_safe=False,
)

