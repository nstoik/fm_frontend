from setuptools import setup, find_packages

__version__ = '0.1'


setup(
    name='fm_frontend',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'fm_frontend = fm_frontend.manage:cli'
        ]
    }
)
