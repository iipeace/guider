SUMMARY = "runtime performance analyzer"
HOMEPAGE = "https://github.com/iipeace/guider"
BUGTRACKER = "https://github.com/iipeace/guider/issues"
AUTHOR = "Peace Lee <ipeace5@gmail.com>"

LICENSE = "GPLv2+"
LIC_FILES_CHKSUM = "file://LICENSE;md5=2c1c00f9d3ed9e24fa69b932b7e7aff2"

SRC_URI = "git://github.com/iipeace/${BPN}"
SRCREV = "ac05a2ce0ab480957d642d947d8f617bd224031d"

S = "${WORKDIR}/git"
R = "${RECIPE_SYSROOT_NATIVE}"

inherit distutils

GUIDER_OBJ = "guider.pyc"
GUIDER_SCRIPT = "guider"

do_install() {
    python ${S}/setup.py install

    install -d ${D}${bindir}
    install -v -m 0755 ${R}/${bindir}/${GUIDER_SCRIPT} ${D}${bindir}/${GUIDER_SCRIPT}

    install -d ${D}${datadir}/${BPN}
    install -v -m 0755 ${R}/${datadir}/${BPN}/${GUIDER_OBJ} ${D}${datadir}/${BPN}/${GUIDER_OBJ}
}

RDEPENDS_${PN} = "python-ctypes python-shell \
                  python-json python-subprocess"

FILES_SOLIBSDEV = ""
#FILES_${PN} = "usr"
