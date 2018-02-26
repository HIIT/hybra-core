#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
  name = 'hybra-core',
  version = '0.1.2a1',
  description = 'Toolkit for data management and analysis.',
  keywords = ['data management', 'data analysis'],
  url = 'https://github.com/HIIT/hybra-core',
  author = 'Matti Nelimarkka, Juho Pääkkönen, Arto Kekkonen',
  author_email = 'matti.nelimarkka@aalto.fi, juho.paakkonen@aalto.fi, arto.kekkonen@helsinki.fi',
  packages = find_packages(exclude=['docs', 'test']),
  package_data={
    'hybra.timeline' : ['*.js', '*.css', '*.html'],
    'hybra.network' : ['*.js', '*.css', '*.html'],
    'hybra.analysis' : ['*.r'],
    'hybra.analysis.topicmodel' : ['*.r', '*.txt']
    },
  licence = 'MIT',


  install_requires=[
    'dateparser>=0.5.1',
    'GitPython>=2.0.6',
    'jupyter>=1.0.0',
    'jupyter_client>=4.3.0',
    'jupyter_console>=4.1.1',
    'jupyter_core>=4.1.0',
    'matplotlib>=1.5.3',
    'nbstripout>=0.2.9',
    'networkx>=1.11',
    'numpy>=1.11.0',
    'requests>=2.9.1',
    'scikit-learn>=0.17.1',
    'scipy>=0.17.1',
    'XlsxWriter>=0.9.6',
    'wordcloud>=1.2.1',
    'tldextract>=2.1.0',
    'pandas>=0.22.0',
    'rpy2<=2.8.6'
  ],

  # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: JavaScript'
  ]
)
