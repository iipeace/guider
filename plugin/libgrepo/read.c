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

int readRepItem(char (*nameList)[NAME_MAX],char (*valueList)[NAME_MAX],int listSize,int flag){
	// now, flag not used
	// all data read, the hierarchy is expressed using '-'
	int fd=g_repFd;
	int file_size;
	char* file_buf;
	int input_len;
	int pos=0;	
	int bracket_num=0;
	int now_list=0;
	int temp_num;
	char direct[NAME_MAX]; 
	char temp_buf[NAME_MAX];
	char old_direct[NAME_MAX];
	// read guider.report and calculate file size
	lseek(fd,0,SEEK_SET);
	file_size = lseek(fd,0,SEEK_END);
	lseek(fd,0,SEEK_SET);
	
	file_buf = malloc(file_size+1);
	
		
	input_len = read(fd,file_buf,file_size);
	
	//parsing start

	while(pos<input_len){
		if(file_buf[pos]=='{'){
			bracket_num++;
			
			pos++;
			if(file_buf[pos]=='}'){
			// condition for '{}'
				pos++;
				bracket_num--;	
				continue;
			}

			while(file_buf[pos]!='"')
				pos++;
			
			pos++;
			temp_num=0;
			while(file_buf[pos]!='"')
			{
				temp_buf[temp_num]=file_buf[pos];
				temp_num++;
				pos++;
			}

			temp_buf[temp_num]=0;
			
			if(bracket_num<=1){
				sprintf(direct,"%s",temp_buf);
				
			}
			else{
				sprintf(direct,"%s-%s",direct,temp_buf);
			
			}
		}
		else if(file_buf[pos]==':'){
			pos=pos+2;
			if(file_buf[pos]=='{')
				continue;
			else{
				if(file_buf[pos]=='"'){//string value
					pos++;
					temp_num=0;
					while(file_buf[pos]!='"')
					{
						temp_buf[temp_num]=file_buf[pos];
						temp_num++;
						pos++;
					}
					temp_buf[temp_num]=0;
					
					sprintf(nameList[now_list],"%s",direct);
					sprintf(valueList[now_list],"%s",temp_buf);
					now_list++;
					// write property and value 
					
				}
				else{//number value
					temp_num=0;
					while(file_buf[pos]>='0'&&file_buf[pos]<='9')
					{
						temp_buf[temp_num]=file_buf[pos];
						temp_num++;
						pos++;
					}
					temp_buf[temp_num]=0;
					
					sprintf(nameList[now_list],"%s",direct);
					sprintf(valueList[now_list],"%s",temp_buf);
					now_list++;
				}
			}
		}
		else if(file_buf[pos]=='"'){
			int len = strlen(direct);
			int i;
			for(i=len-1;i>=0;i--){
				if(direct[i]=='-'){
					direct[i]=0;
					break;
				}
			}
			
			temp_num=0;
			pos++;
			while(file_buf[pos]!='"')
			{
				temp_buf[temp_num]=file_buf[pos];
				temp_num++;
				pos++;
			}
			temp_buf[temp_num]=0;
			if(bracket_num<=1)
				sprintf(direct,"%s",temp_buf);
			else
				sprintf(direct,"%s-%s",direct,temp_buf);
			
			pos=pos+3;
			if(file_buf[pos]=='{')
				continue;
			else{
				if(file_buf[pos]=='"'){//string value
					pos++;
					temp_num=0;
					while(file_buf[pos]!='"')
					{
						temp_buf[temp_num]=file_buf[pos];
						temp_num++;
						pos++;
					}
					temp_buf[temp_num]=0;
					
					sprintf(nameList[now_list],"%s",direct);
					sprintf(valueList[now_list],"%s",temp_buf);
					now_list++;
					// write property and value 
					
				}
				else{//number value
					temp_num=0;
					while(file_buf[pos]>='0'&&file_buf[pos]<='9')
					{
						temp_buf[temp_num]=file_buf[pos];
						temp_num++;
						pos++;
					}
					temp_buf[temp_num]=0;
					
					sprintf(nameList[now_list],"%s",direct);
					sprintf(valueList[now_list],"%s",temp_buf);
					now_list++;
				}
			}
		}
		else if(file_buf[pos]=='}'){
			bracket_num--;
			int len = strlen(direct);
			int i;
			for(i=len-1;i>=0;i--){
				if(direct[i]=='-'){
					direct[i]=0;
					break;
				}
			}
			if(bracket_num==1)
				direct[0]=0;
		}
		pos++;
		if(now_list>=listSize)
			break;
	}
	return now_list;
}
