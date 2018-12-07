import site, os, sys
from distutils.core import setup

setup(
    name = 'guider',
    version = '3.9.4',
    license = 'GPL2',
    description = 'A system-wide analyzer of performance',
    author = 'Peace Lee',
    author_email = 'iipeace5@gmail.com',
    url = 'https://github.com/iipeace/guider',
    download_url = 'https://github.com/iipeace/guider/archive/master.zip',
    keywords = ['guider', 'linux', 'analyzer', 'performance', 'profile', 'trace', 'kernel'],
    packages = ['guider'],
    scripts = ['guider/guider'],
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

# make guider directory #
try:
    desPath = '%s/share/guider' % sys.prefix
    pycDesPath = '%s/guider.pyc' % desPath
    os.mkdir(desPath)
except:
    pass

# search package path #
for path in site.getsitepackages():
    # check path #
    if os.path.isdir('%s/guider' % path) is False:
        continue

    # set pyc source path #
    pycSrcPath = '%s/guider/guider.pyc' % path

    try:
        # prepare source pyc file #
        pycTmpPath = '%s/guider/__pycache__/' % path
        if os.path.isdir(pycTmpPath):
            for cache in os.listdir(pycTmpPath):
                os.rename('%s%s' % (pycTmpPath, cache), pycSrcPath)

        # check pyc source file #
        if os.path.isfile(pycSrcPath) is False:
            continue

        # remove old pyc file #
        if os.path.isfile(pycDesPath):
            os.unlink(pycDesPath)

        # create pyc destination path #
        os.symlink(pycSrcPath, pycDesPath)
    except:
        pass

'''
pypi upload command
    # python setup.py sdist upload -r pypitest
    # python setup.py sdist upload -r https://upload.pypi.org/legacy/
'''
