from setuptools import setup

from hobo import __version__


setup(
    name='hobo',
    version=__version__,
    description='A simple module for reading Onset HOBO data logger data',
    long_description=open('README.txt').read(),
    url='https://github.com/nationalparkservice/hobo-py',
    author='David A. Riggs',
    author_email='david_a_riggs@nps.gov',
    py_modules=['hobo'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: Public Domain',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    ],
)
