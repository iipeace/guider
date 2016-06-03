/*
 * Getting memory map about file page on memory
 *
 * Copyright (c) 2016 Peace Lee <iipeace5@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/syscall.h>

static unsigned char *table = NULL;

unsigned char *get_loadPageMap(int fd) {
	int idx;
	void *file_mmap;
	struct stat file_stat;
	ssize_t page_size = getpagesize();
	ssize_t table_size;

	if (table != NULL) {
		free(table);
	}

	if (fstat(fd, &file_stat) < 0) {
		printf("Fail to fstat\n");
		return NULL;
	}

	if ( file_stat.st_size == 0 ) {
		printf("Fail to get file size\n");
		return NULL;
	}

	file_mmap = mmap((void *)0, file_stat.st_size, PROT_NONE, MAP_SHARED, fd, 0);

	if (file_mmap == MAP_FAILED) {
		printf("Fail to mmap\n");
		return NULL;
	}

	table_size = (file_stat.st_size + page_size - 1) / page_size;
	table = calloc(1, table_size);

	if (table == NULL) {
		printf("Fail to calloc\n");
		return NULL;
	}

	if (mincore(file_mmap, file_stat.st_size, table) != 0) {
		printf("Fail to mincore\n");
		return NULL;
	}

	for (idx = 0; idx < table_size; idx++) {
		table[idx] &= 1;
	}

	munmap(file_mmap, file_stat.st_size);

	return table;
}

int save_pipeToFile(char *inFile, char *outFile) {
	int ret;
	int pipefd[2];
	int in_fd, out_fd;
	size_t maxReadSize = 1048576;

	ret = pipe(pipefd);
	if (ret < 0) {
		printf("Fail to open pipe\n");
		return -1;
	}

	in_fd = open(inFile, O_RDONLY);
	if (in_fd < 0){
		printf("Fail to open %s\n", inFile);
		return -1;
	}

	out_fd = open(outFile, O_CREAT | O_TRUNC | O_RDWR | O_DIRECT);
	if (out_fd < 0){
		printf("Fail to open %s\n", outFile);
		return -1;
	}

	while(1){
		sleep(1);

		ret = splice(in_fd, 0, pipefd[1], NULL, maxReadSize, SPLICE_F_MORE | SPLICE_F_MOVE);

		ret = splice(pipefd[0], NULL, out_fd, 0, maxReadSize, SPLICE_F_MORE | SPLICE_F_MOVE);

		if (ret <= 0)
			break;
	}

	close(pipefd[0]);
	close(pipefd[1]);

	close(in_fd);
	close(out_fd);

	return 0;
}

