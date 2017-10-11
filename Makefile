# Makefile to build objects of guider
#
# Copyright (c) 2016-2017 Peace Lee <iipeace5@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.


ifneq ($(KERNELRELEASE),)
	obj-m := guiderMod.o
else
	CFLAGS = -fPIC
	LDFLAGS = -shared
endif

CC = gcc 
RM = rm -f
TARGET_BIN = guider
TARGET_LIB = libguider.so

ifneq ($(wildcard .config),)
  include .config
endif

prefix ?= /usr

PCC = $(shell which python)
PFLAGS = -m py_compile
TARGET_PY = guider.py
TARGET_PYC = guider.pyc
INSTALL_DIR = $(prefix)/share/guider
SBIN_DIR = $(prefix)/sbin
LIB_DIR = $(prefix)/lib

SRCS = guiderLib.c
OBJS = $(SRCS:.c=.o)

KPATH := /lib/modules/$(shell uname -r)/build



.PHONY: all
all: ${TARGET_LIB} ${TARGET_PYC}

$(TARGET_PYC): $(TARGET_PY)
		@test -s ${PCC} || { echo "Fail to compile guider"; false; }
		$(PCC) $(PFLAGS) $^

$(TARGET_LIB): $(OBJS)
		$(CC) ${LDFLAGS} -o $@ $^

.PHONY: install
install: all
	@mkdir -p ${INSTALL_DIR} ${SBIN_DIR} ${LIB_DIR}
	@cp ${TARGET_PYC} ${INSTALL_DIR}/ || { echo "Fail to install into ${INSTALL_DIR}"; false; }
	@cp ${TARGET_BIN} ${SBIN_DIR}/ || { echo "Fail to install into ${SBIN_DIR}"; false; }
	@cp ${TARGET_LIB} ${LIB_DIR}/ || { echo "Fail to install into ${LIB_DIR}"; false; }
	@sed -i "s%PREFIX_DIR=%PREFIX_DIR=$(prefix)%g" ${SBIN_DIR}/${TARGET_BIN}

.PHONY: kernel
kernel: all
	@make -C $(KPATH) M=$(PWD) modules

.PHONY: clean
clean:
	@-${RM} -f ${TARGET_LIB} ${OBJS} $(SRCS:.c=.d)
	@-${RM} -f ${TARGET_PYC}
	@-${RM} -f ${INSTALL_DIR}/*
	@-${RM} -f ${SBIN_DIR}/${TARGET_BIN}
	@-${RM} -f ${LIB_DIR}/${TARGET_LIB}
	@make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
