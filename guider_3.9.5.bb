SUMMARY = "runtime performance analyzer"
HOMEPAGE = "https://github.com/iipeace/guider"
BUGTRACKER = "https://github.com/iipeace/guider/issues"
AUTHOR = "Peace Lee <ipeace5@gmail.com>"

LICENSE = "GPLv2+"
LIC_FILES_CHKSUM = "file://LICENSE;md5=2c1c00f9d3ed9e24fa69b932b7e7aff2"

PV = "3.9.5+git${SRCPV}"
PR = "r0"

SRC_URI = "git://github.com/iipeace/${BPN}"
#SRCREV = "${AUTOREV}"
SRCREV = "534f385a86b6be105a6519f4c87f230e1a10d408"

S = "${WORKDIR}/git"
R = "${RECIPE_SYSROOT}"

inherit distutils

GUIDER_OBJ = "guider.pyc"
GUIDER_SCRIPT = "guider"

do_install() {
    python ${S}/setup.py install

    install -d ${D}${bindir}
    install -v -m 0755 ${STAGING_BINDIR_NATIVE}/${GUIDER_SCRIPT} ${D}${bindir}/${GUIDER_SCRIPT}

    install -d ${D}${datadir}/${BPN}
    install -v -m 0755 ${STAGING_LIBDIR_NATIVE}/python${PYTHON_BASEVERSION}/site-packages/${BPN}/${GUIDER_OBJ} ${D}${datadir}/${BPN}/${GUIDER_OBJ}
}

RDEPENDS_${PN} = "python-ctypes python-shell \
                  python-json python-subprocess"
