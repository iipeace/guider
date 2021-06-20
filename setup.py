from setuptools import setup, find_packages
import site, os, sys, shutil

setup(
    name = 'guider',
    version = '3.9.84',
    license = 'GPL2',
    description = 'A system-wide analyzer of performance',
    author = 'Peace Lee',
    author_email = 'iipeace5@gmail.com',
    url = 'https://github.com/iipeace/guider',
    download_url = 'https://github.com/iipeace/guider/archive/master.zip',
    packages = find_packages(exclude = ['tests*']),
    keywords = ['guider', 'linux', 'analyzer', 'performance', 'profile', 'trace', 'kernel'],
    scripts = ['guider/guider'],
    zip_safe=False,
    classifiers = [
        'Environment :: Console',
        'Programming Language :: Python',
        'Operating System :: Android',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: System :: Filesystems',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Operating System Kernels',
        ],
)

'''
build & install command
    # python3 -m pip install setuptools wheel
    # python3 setup.py build
    # python3 setup.py install
pypi upload command
    # sudo python3 -m pip install twine
    # rm dist/* -rf
    # sudo python3 setup.py sdist bdist_wheel
    # python3 -m twine upload --repository pypi dist/*
    # python3 -m twine upload --repository pypitest dist/*
'''
