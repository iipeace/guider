
CC = gcc 
CFLAGS = -fPIC
LDFLAGS = -shared
RM = rm -f
TARGET_LIB = libguider.so

PCC = python
COMP = -m py_compile
TARGET_PY = guider.py
TARGET_PYC = guider.pyc

SRCS = guider.c
OBJS = $(SRCS:.c=.o)

.PHONY: all
all: ${TARGET_LIB} ${TARGET_PYC}

$(TARGET_PYC): $(TARGET_PY)
		$(PCC) $(COMP) $^

$(TARGET_LIB): $(OBJS)
		$(CC) ${LDFLAGS} -o $@ $^

$(SRCS:.c=.d):%.d:%.c
		$(CC) $(CFLAGS) -MM $< >$@

#include $(SRCS:.c=.d)

.PHONY: clean
clean:
	-${RM} ${TARGET_LIB} ${OBJS} $(SRCS:.c=.d)
	-${RM} ${TARGET_PYC}
