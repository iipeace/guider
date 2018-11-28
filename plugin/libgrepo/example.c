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

#define LIST_MAX 150 

int main(void){
	char list[LIST_MAX][NAME_MAX];	
	char value[LIST_MAX][NAME_MAX];
	int list_len;
	int i;

	openRepFile("/home/bychoi/guider/guider/guider.report");

	list_len=readRepItem(list,value,LIST_MAX,0);
	printf("list len : %d\n",list_len);
	for(i=0;i<list_len;i++){
		printf("%s : %s\n",list[i],value[i]);
	}	

	closeRepFile();
	
	return 0;
} 
