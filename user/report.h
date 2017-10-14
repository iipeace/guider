/*
 * Interfaces in report library
 *
 * Copyright (c) 2017 Peace Lee <iipeace5@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 */

#ifndef __GUIDER_REPLIB_H__
#define __GUIDER_REPLIB_H__

#define NAME_MAX 32

#include <stdio.h>
#include <fcntl.h>
#include <pthread.h>

#endif

// file interface
int g_repFd;
int openRepFile(const char *path);
int readRepData(char (*list)[NAME_MAX], int listSize);
int closeRepFile(void);

// read interface
enum guider_report_read_bits {
    GRR_WAIT,
    GRR_THREAD,
    GRR_COND,
    GRR_MAX,
}

int g_repType;
int initRepFile(const char *path);
int initRepSocket(const char *serverIP, int serverPort, int clientPort);
int readRepItem(const char (*nameList)[NAME_MAX], char (*valueList)[NAME_MAX], int listSize, int flag);
int addRepCond(void);
int removeRepCond(void);
int cleanRep(void);

