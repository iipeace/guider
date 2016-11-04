# Makefile to build libguider.so and guider.pyc
#
# Copyright (c) 2016 Peace Lee <iipeace5@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.


CC = gcc 
CFLAGS = -fPIC
LDFLAGS = -shared
RM = rm -f
TARGET_LIB = libguider.so

PCC = $(shell which python)
PFLAG = -m py_compile
TARGET_PY = guider.py
TARGET_PYC = guider.pyc
INSTALL_DIR = /usr/share/guider

SRCS = guider.c
OBJS = $(SRCS:.c=.o)

.PHONY: all
all: ${TARGET_LIB} ${TARGET_PYC}

$(TARGET_PYC): $(TARGET_PY)
		@test -s ${PCC} || { echo "Fail to compile guider"; false; }
		$(PCC) $(PFLAG) $^

$(TARGET_LIB): $(OBJS)
		$(CC) ${LDFLAGS} -o $@ $^

.PHONY: install
install: all
	@test -s ${INSTALL_DIR} || mkdir ${INSTALL_DIR}
	@test -s ${INSTALL_DIR} || { echo "Fail to make ${INSTALL_DIR}"; false; }
	@cp ${TARGET_PYC} ${INSTALL_DIR}/ || { echo "Fail to install into ${INSTALL_DIR}"; false; }

.PHONY: clean
clean:
	@-${RM} ${TARGET_LIB} ${OBJS} $(SRCS:.c=.d)
	@-${RM} ${TARGET_PYC}
	@-${RM} ${INSTALL_DIR}/*
