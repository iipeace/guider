/*
 * Functions to read report data from file in report library
 *
 * Copyright (c) 2017 Peace Lee <iipeace5@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 */

#include "report.h"

int openRepFile(const char *path){
	int fd;
	fd = open(path,O_RDONLY);
	
	if(fd == -1){
		g_repFd=-1;
		return -1;
	}
	else{
		g_repFd=fd;
		return 0;
	}

}

int readRepData(char (*list)[NAME_MAX],int listSize){
	//temporary execution for test 

	if(g_repFd == -1)
		return -1;
	// test before parsing
	char buf[50];
	int slen=read(g_repFd,buf,49);
	buf[slen]='\0';
	printf("%s\n",buf);
	
	return 0;
}

int closeRepFile(void){
	if(g_repFd == -1)
		return -1;
	
	close(g_repFd);
	
	return 0;
}

