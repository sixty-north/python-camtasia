from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='camtasia',
    version="6.1.2",
    packages=find_packages('src'),

    author='Sixty North AS',
    author_email='austin@sixty-north.com',
    description='Python API for Camtasia projects',
    license='MIT',
    keywords='',
    url='https://github.com/sixty-north/python-camtasia',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ],
    platforms='any',
    # include_package_data=True,
    package_dir={'': 'src'},
    package_data={'camtasia': ['resources/**']},
    install_requires=[
        'exit-codes >=1.3.0, < 2.0.0',
        'docopt-subcommands',
        'pymediainfo',
        'marshmallow',
        'marshmallow-oneofschema',
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax, for
    # example: $ pip install -e .[dev,test]
    extras_require={
        'dev': ['bumpversion'],
        # 'doc': ['sphinx', 'cartouche'],
        'test': ['hypothesis', 'pytest'],
    },
    entry_points={
        'console_scripts': [
           'pytsc = camtasia.cli:main',
        ],
    },
    long_description=Path('README.rst').read_text(),
)
