from setuptools import setup, find_packages
import site, os, sys, shutil

setup(
    name = 'guider',
    version = '3.9.896',
    license = 'GPL2',
    description = 'Unified performance analyzer',
    author = 'Peace Lee',
    author_email = 'iipeace5@gmail.com',
    url = 'https://github.com/iipeace/guider',
    download_url = 'https://github.com/iipeace/guider/archive/master.zip',
    packages = find_packages(exclude = ['tests*']),
    keywords = ['guider', 'linux', 'analyzer', 'performance', 'profile', 'trace', 'kernel'],
    scripts = ['guider/guider'],
    data_files = [("guider", ["guider/guider.conf"])],
    zip_safe=False,
    install_requires = ['psutil; platform_system!="Linux"'],
    classifiers = [
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: Android',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Filesystems',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Operating System Kernels :: Linux',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        ],
)

'''
build & install command
    # python3 -m pip install setuptools wheel
    # python3 setup.py build
    # python3 setup.py install
pypi upload command
    # sudo python3 -m pip install twine wheel
    # rm dist/* -rf
    # sudo python3 setup.py sdist bdist_wheel
    # python3 -m twine upload --repository pypi dist/*
    # python3 -m twine upload --repository pypitest dist/*
'''
