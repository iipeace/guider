/*
 * Example program for report library
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

#define LIST_MAX 50 

int main(void){
	char list[LIST_MAX][NAME_MAX];	
	
	openRepFile("/home/bychoi/guider/guider/guider.report");
	
	readRepData(list,LIST_MAX);

	closeRepFile();
	
	return 0;
} 
