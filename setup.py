from setuptools import setup
from setuptools import find_packages
def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='planet_batch',
    version='0.1.1',
    package_data={'planet_batch': ['aoi.json']},
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
