"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='treepy',

    version='0.1',

    description='Python library for programmatic interaction with tree.mu',
    long_description=long_description,

    url='https://github.com/ianalis/treepy',

    author='Christian Alis',
    author_email='c.alis@ucl.ac.uk',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='tree.mu data science',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['pandas', 'numpy', 'seaborn'],
)