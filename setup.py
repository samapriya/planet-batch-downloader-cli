import subprocess
import os
import sys
import setuptools
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
from distutils.version import StrictVersion
from setuptools import __version__ as setuptools_version

if StrictVersion(setuptools_version) < StrictVersion('38.3.0'):
    raise SystemExit(
        'Your `setuptools` version is old. '
        'Please upgrade setuptools by running `pip install -U setuptools` '
        'and try again.'
    )

try:
    subprocess.call(['git'],shell=True)
    subprocess.call('pip install git+https://github.com/planetlabs/planet-client-python.git --force',shell=True)
except OSError as e:
    if e.errno==os.errno.ENOENT:
        raise SystemExit(
            'Git not found Install Git '
            'and try again.'
        )
    else:
        sys.exit("Git not found Install Git "+str(e))
def readme():
    with open('README.md') as f:
        return f.read()
setuptools.setup(
    name='planet_batch',
    version='0.1.1',
    package_data={'planet_batch': ['aoi.json','idpl.csv','idpl.txt']},
    include_package_data=True,
    packages=find_packages(),
    install_requires=['psutil>=5.2.2','urllib3>=1.22','requests>=2.18.4','retrying>=1.3.3',
'progressbar2>=3.34.2','pyshp>=1.2.12'],
    url='https://github.com/samapriya/planet-batch-downloader-cli',
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ),
    author='Samapriya Roy',
    author_email='samapriya.roy@gmail.com',
    description='planet batch downloader cli',
    entry_points={
        'console_scripts': [
            'planet_batch=planet_batch.planet_batch:main',
        ],
    },
)
