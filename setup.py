import os

import setuptools

VERSION = '0.0.2'

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="magmalt",
    version=VERSION,
    author="Vassil Verguilov",
    author_email="Vassil.Verguilov@gmail.com",
    description=
    "Simple Machine Learning pipeline tools for Major Atmospheric Gamma Imaging Cherenkov Telescopes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    install_requires=[
        'numpy>1.17',
        'numexpr',
        'pandas>=1.0.3',
        'sklearn',
        'scikit-learn',
        'tqdm',
        'pyyaml>=5.3.1',
        'pydantic',
        'uproot>=3.11.3',
        'colorama',
        'coloredlogs',
    ],
    extras_require={  # Optional
        'dev': ['yapf'],
        'tests': ['pytest', 'pytest-cov', 'coverage'],
        'xgboost': ['xgboost>=1.0.2'],
        'keras': ['tensorflow>2.0.0']
    },
    entry_points={
        'console_scripts': [
            'magmalt=magmalt.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)