# Makefile to build objects of guider
#
# Copyright (c) 2016-2018 Peace Lee <iipeace5@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

ifneq ($(findstring $(MAKEFLAGS),s),s)
  ifneq ($(V),1)
	QUIET_CC       = @echo '  CC       '$(patsubst $(objdir)/%,%,$@);
	QUIET_PCC      = @echo '  PCC      '$(patsubst $(objdir)/%,%,$@);
	QUIET_LINK     = @echo '  LINK     '$(patsubst $(objdir)/%,%,$@);
	QUIET_MKDIR    = @echo '  MKDIR    '$(patsubst $(objdir)/%,%,$@);
	QUIET_GEN      = @echo '  GEN      '$(patsubst $(objdir)/%,%,$@);

	QUIET_CLEAN    = @printf '  CLEAN    %s\n' $1;
	QUIET_INSTALL  = @printf '  INSTALL  %s\n' $1;
	QUIET_UNINSTALL= @printf '  REMOVE   %s\n' $1;

	Q = @
  endif
endif

ifneq ($(KERNELRELEASE),)
	obj-m := guiderMod.o
else
    ifneq ($(MAKECMDGOALS),clean)
      CFLAGS = -fPIC
      LDFLAGS = -shared
      CPPFLAGS := $(shell python-config --includes)
      PCC = $(shell which python)
      PFLAGS = -m py_compile

      ifeq ($(CPPFLAGS),)
        $(warning "Fail to find Python.h so that requires CPPFLAGS variable")
      endif
      ifeq ($(PCC),)
        $(error "Fail to find python so that requires PCC variable")
      endif
    endif
endif

CC = gcc 
RM = rm -f
MV = mv -f
INSTALL = install
SED = sed

MODULE = guider
TARGET_BIN = guider
TARGET_LIB = guidermodule.so

ifneq ($(wildcard .config),)
  include .config
endif

prefix ?= /usr

TARGET_PY = guider.py
TARGET_PYC = guider.pyc
INSTALL_DIR = $(prefix)/share/guider
SBIN_DIR = $(prefix)/sbin
LIB_DIR = $(prefix)/lib

SRCS = guiderLib.c
OBJS = guiderLib.o

KPATH := /lib/modules/$(shell uname -r)/build


.PHONY: all
all: $(TARGET_PYC) $(OBJS) $(TARGET_LIB)

$(TARGET_PYC): $(TARGET_PY)
	$(QUIET_PCC)$(PCC) $(PFLAGS) $^
	$(Q)if [ -f __pycache__/$(MODULE)*.pyc ]; then \
		$(MV) __pycache__/$(MODULE)*.pyc $(CURDIR)/$(MODULE).pyc; \
	fi

$(OBJS): $(SRCS)
	$(QUIET_CC)$(CC) $(CFLAGS) $(CPPFLAGS) -c -o $@ $^

$(TARGET_LIB): $(OBJS)
	$(QUIET_CC)$(CC) $(LDFLAGS) -o $@ $(OBJS)

.PHONY: install
install: all
	$(Q)$(INSTALL) -d -m 755 $(INSTALL_DIR)
	$(Q)$(INSTALL) -d -m 755 $(SBIN_DIR)
	$(Q)$(INSTALL) -d -m 755 $(LIB_DIR)

	$(call QUIET_INSTALL, $(TARGET_PYC))
	$(Q)$(INSTALL) $(TARGET_PYC) $(INSTALL_DIR)/$(TARGET_PYC)

	$(call QUIET_INSTALL, $(TARGET_BIN))
	$(Q)$(INSTALL) $(TARGET_BIN) $(SBIN_DIR)/$(TARGET_BIN)

	$(call QUIET_INSTALL, $(TARGET_LIB))
	$(Q)$(INSTALL) $(TARGET_LIB) $(LIB_DIR)/$(TARGET_LIB)
	$(Q)$(SED) -i "s%PREFIX_DIR=%PREFIX_DIR=$(prefix)%g" $(SBIN_DIR)/$(TARGET_BIN)

.PHONY: kernel
kernel: all
	-$(Q)$(MAKE) -C $(KPATH) M=$(PWD) modules

.PHONY: clean
clean:
	$(call QUIET_CLEAN, guider)
	$(Q)$(RM) $(TARGET_LIB) $(OBJS)
	$(Q)$(RM) $(TARGET_PYC)
	$(Q)$(RM) $(INSTALL_DIR)/*
	$(Q)$(RM) $(SBIN_DIR)/$(TARGET_BIN)
	$(Q)$(RM) $(LIB_DIR)/$(TARGET_LIB)

	$(call QUIET_CLEAN, kernel-module)
	-$(Q)if [ -d /lib/modules/$(shell uname -r)/build ]; then \
		$(MAKE) -sC /lib/modules/$(shell uname -r)/build M=$(PWD) clean; \
	fi
