# Makefile to build report library for user application
#
# Copyright (c) 2017 Peace Lee <iipeace5@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

report : file.o read.o job.o socket.o thread.o
	ar rc libreport.a file.o read.o job.o socket.o thread.o
	ranlib libreport.a 

file.o : report.h file.c
	gcc -c file.c

read.o : report.h read.c
	gcc -c read.c

job.o : report.h job.c
	gcc -c job.c

socket.o : report.h socket.c
	gcc -c socket.c

thread.o : report.h thread.c
	gcc -c thread.c

clean : 
	rm *.o libreport.a

