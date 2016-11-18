# Makefile to build objects of guider
#
# Copyright (c) 2016 Peace Lee <iipeace5@gmail.com>
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
TARGET_LIB = libguider.so

PCC = $(shell which python)
PFLAGS = -m py_compile
TARGET_PY = guider.py
TARGET_PYC = guider.pyc
INSTALL_DIR = /usr/share/guider

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
	@test -s ${INSTALL_DIR} || mkdir ${INSTALL_DIR}
	@test -s ${INSTALL_DIR} || { echo "Fail to make ${INSTALL_DIR}"; false; }
	@cp ${TARGET_PYC} ${INSTALL_DIR}/ || { echo "Fail to install into ${INSTALL_DIR}"; false; }

.PHONY: kernel
kernel: all
	@make -C $(KPATH) M=$(PWD) modules

.PHONY: clean
clean:
	@-${RM} ${TARGET_LIB} ${OBJS} $(SRCS:.c=.d)
	@-${RM} ${TARGET_PYC}
	@-${RM} ${INSTALL_DIR}/*
	@make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
