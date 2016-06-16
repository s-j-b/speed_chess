/* Chess Client
 * by Simon J. Bloch
 *
 * Created: 1/22/2016
 */

#include <arpa/inet.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdio.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

/*##############################################################################
################################### Globals ####################################
##############################################################################*/

#define MOVE_SIZE (4)
#define DIM (8)
#define BACKLOG (10)
#define REQUEST_SIZE (6)
#define printhere printf("HERE--> %d\n", __LINE__)

char move[MOVE_SIZE];

/*##############################################################################
################################# Declarations #################################
##############################################################################*/

char connectPlayers(int sock);
void playGame(char color, int sock);
void sendBuffer(char* buffer, int size, int sock);
void recvBuffer(char* buffer, int size, int sock);

/*##############################################################################
################################## Functions ###################################
##############################################################################*/

int main(int argc, char** argv) {
    
    // Check and parse args
    if (argc != 3) {
        printf("Usage:\n%s <ip addr> <port>\n", argv[0]);
        exit(1);
    }
    int port = atoi(argv[2]);
    
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    
    if(sock < 0) {
        perror("socket");
        exit(1);
    }

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = inet_addr(argv[1]);

    // Initiate server connection
    int ret = connect(sock, (struct sockaddr*)&addr, sizeof(addr));
    if(ret < 0) {
        perror("connect");
        exit(1);
    }

    char color = connectPlayers(sock);
    playGame(color, sock);
}    

char connectPlayers(int sock) {

    char* connection;
    connection = malloc(REQUEST_SIZE);
    memset(connection, 0, REQUEST_SIZE);
    
    scanf("%s", connection);
    
    sendBuffer(connection, REQUEST_SIZE, sock);

    return connection[5];
}
    
void playGame(char color, int sock) {
    if (color == 'W') {
        while(1) {
            scanf("%s", move);
            sendBuffer(move, MOVE_SIZE, sock);
            if (!strcmp(move, "mate")) {
                break;
            }
            
            recvBuffer(move, MOVE_SIZE, sock);
            if (!strcmp(move, "mate")) {
                break;
            }
        }
    } else {
        while(1) {
            recvBuffer(move, MOVE_SIZE, sock);
            if (!strcmp(move, "mate")) {
                break;
            }

            scanf("%s", move);
            sendBuffer(move, MOVE_SIZE, sock);
            if (!strcmp(move, "mate")) {
                break;
            }            
        }
    }    
}

void sendBuffer(char* buffer, int size, int sock) {
    int totSent = 0;
    while (totSent < size) {
        int sendCount = send(sock, buffer + totSent, size - totSent, 0);
        if (sendCount < 0) {
            perror("send");
            exit(1);
        }
        totSent += sendCount;
    }
}

void recvBuffer(char* buffer, int size, int sock) {
    int recv_count = 0;
    while((recv_count += recv(sock, buffer + recv_count,
                              size - recv_count, 0)) > 0) {
        if (recv_count >= size) {
            buffer[size] = '\0';
            printf("IN: %s\n", buffer);
            break;
        }
    }
}
    
