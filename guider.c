#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
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

