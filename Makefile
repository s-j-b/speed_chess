TARGETS=chess_server chess_client

CFLAGS=-Wall -g -O0

all: $(TARGETS)

chess_server: chess_server.c
	gcc $(CFLAGS) -o chess_server chess_server.c

chess_client: chess_client.c
	gcc $(CFLAGS) -o chess_client chess_client.c

clean:
	rm -f $(TARGETS)
