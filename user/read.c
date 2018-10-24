/*
 * Functions to manage report data in report library
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

int initRepFile(const char *path){
// now just open file
	return openRepFile(path);
}

int readRepItem(const char (*nameList)[NAME_MAX],char (*valueList)[NAME_MAX],int listSize,int flag){
	// now, flag not used
	// all data read, the hierarchy is expressed using '-'
	int fd=g_repFd;
	int file_size;
	char* file_buf;
	int input_len;
	 
	lseek(fd,0,SEEK_SET);
	file_size = lseek(fd,0,SEEK_END);
	lseek(fd,0,SEEK_SET);
	
	file_buf = malloc(file_size+1);
	
		
	input_len = read(fd,file_buf,file_size);
	
	//parsing start

	return 0;
}
	

