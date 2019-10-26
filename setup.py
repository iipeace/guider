import site, os, sys, shutil
from distutils.core import setup

setup(
    name = 'guider',
    version = '3.9.6',
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
    if not os.path.isdir('%s/guider' % path):
        continue

    # set pyc source path #
    pycSrcPath = '%s/guider/guider.pyc' % path

    try:
        # prepare source pyc file #
        pycTmpDir = '%s/guider/__pycache__/' % path
        if os.path.isdir(pycTmpDir):
            for cache in os.listdir(pycTmpDir):
                if not cache.startswith('guider'):
                    continue

                # rename cpython-format name #
                pycTmpFile = '%s%s' % (pycTmpDir, cache)
                os.rename(pycTmpFile, pycSrcPath)

        # check pyc source file #
        if not os.path.isfile(pycSrcPath):
            continue

        # remove old pyc file #
        if os.path.isfile(pycDesPath):
            os.unlink(pycDesPath)

        # create pyc destination path #
        os.symlink(pycSrcPath, pycDesPath)

        print("Wrote %s and linked it to %s successfully" % \
            (pycSrcPath, pycDesPath))
    except:
        err = sys.exc_info()[1]

        try:
            if len(err.args) == 0 or err.args[0] == 0:
                #print(sys.exc_info()[0].__name__)
                continue
            errRes = ' '.join(list(map(str, err.args)))
            print("[ERROR] Fail to write %s and link it to %s" % \
                (pycSrcPath, pycDesPath))
        except:
            pass

'''
pypi upload command
    # python setup.py sdist upload -r pypitest
    # python setup.py sdist upload -r https://upload.pypi.org/legacy/
'''
