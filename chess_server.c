/* Chess Server
 * by Simon J. Bloch
 *
 * Created: 1/19/2016
 */

#include <arpa/inet.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <inttypes.h>
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
#define printhere printf("@LINE: %d\n", __LINE__)

int move_number;
int is_white;
char board[DIM][DIM];

char move[MOVE_SIZE];

/*##############################################################################
################################# Declarations #################################
##############################################################################*/

int initializeServer(int port_num);
void connectPlayers(int server_sock);
void playGame(char color, int sock);
void recvBuffer(char* buffer, int size, int sock);
void sendBuffer(char* buffer, int size, int sock);

/*##############################################################################
################################## Functions ###################################
##############################################################################*/

int main(int argc, char **argv) {

    // Check and parse args
    if (argc != 2) {
        printf("Usage:\n%s <port>\n", argv[0]);
        exit(1);
    }
    int port = atoi(argv[1]);

    // Initialize server
    int sock = initializeServer(port);

    connectPlayers(sock);

    close(sock);

    exit(0);
}

int initializeServer(int port_num) {

    /* Get the port number from the arguments. */
    uint16_t port = (uint16_t) port_num;
    
    int ret;

    // Create Socket
    int server_sock = socket(AF_INET, SOCK_STREAM, 0);
    if(server_sock < 0) {
        perror("Creating socket failed");
        exit(1);
    }

    /* A server socket is bound to a port, which it will listen on for incoming
     * connections.  By default, when a bound socket is closed, the OS waits a
     * couple of minutes before allowing the port to be re-used.  This is
     * inconvenient when you're developing an application, since it means that
     * you have to wait a minute or two after you run to try things again, so
     * we can disable the wait time by setting a socket option called
     * SO_REUSEADDR, which tells the OS that we want to be able to immediately
     * re-bind to that same port. See the socket(7) man page ("man 7 socket")
     * and setsockopt(2) pages for more details about socket options. */
    int reuse_true = 1;
    ret = setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, &reuse_true,
                     sizeof(reuse_true));

    if (ret < 0) {
        perror("Setting socket option failed");
        exit(2);
    }

    /* Create an address structure.  This is very similar to what we saw on the
     * client side, only this time, we're not telling the OS where to connect,
     * we're telling it to bind to a particular address and port to receive
     * incoming connections.  Like the client side, we must use htons() to put
     * the port number in network byte order.  When specifying the IP address,
     * we use a special constant, INADDR_ANY, which tells the OS to bind to all
     * of the system's addresses.  If your machine has multiple network
     * interfaces, and you only wanted to accept connections from one of them,
     * you could supply the address of the interface you wanted to use here. */
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = INADDR_ANY;

    // Tell OS to bind socket to address and port specified above.
    ret = bind(server_sock, (struct sockaddr *)&addr, sizeof(addr));
    if (ret < 0) {
        perror("Error binding to port");
        exit(3);
    }

    /* Now that we've bound to an address and port, we tell the OS that we're
     * ready to start listening for client connections.  This effectively
     * activates the server socket.  BACKLOG (#defined above) tells the OS how
     * much space to reserve for incoming connections that have not yet been
     * accepted. */
    ret = listen(server_sock, BACKLOG);
    if (ret < 0) {
        perror("Error listening for connection");
        exit(4);
    }

    return server_sock;
}

void connectPlayers(int server_sock) {
    printf("GAME ON\n");
    while(1) {

        // Declare a socket for the client connection.
        int sock;

        // Another address structure. The system will fill it in when we accept
        // a connection.
        struct sockaddr_in remote_addr;
        unsigned int socklen = sizeof(remote_addr);

        /* Accept the first waiting connection from the server socket and
         * populate the address information.  The result (sock) is a socket
         * descriptor for the conversation with the newly connected client.  If
         * there are no pending connections in the back log, this function will
         * block indefinitely while waiting for a client connection to be made.
         * */
        sock = accept(server_sock, (struct sockaddr *) &remote_addr, &socklen);
        if(sock < 0) {
            perror("Error accepting connection");
            exit(1);
        }
        
        char buffer[REQUEST_SIZE + 1];
        memset(buffer, 0, sizeof(buffer));

        int recv_count = 0;
        while((recv_count += recv(sock, buffer + recv_count,
                                  REQUEST_SIZE - recv_count, 0)) > 0) {
            if (recv_count >= REQUEST_SIZE) {
                buffer[REQUEST_SIZE] = '\0';
                break;
            }
        }

        int b = strcmp(buffer, "chessB");
        int w = strcmp(buffer, "chessW");

        if (w & b) {
            perror("Invalid color choice.");
            exit(1);
        } else {
            if (w) {
                playGame('b', sock);
            } else {
                playGame('w', sock);
            }
        }
    }
    
    printf("GAME OFF\n");
}

void playGame(char color, int sock) {
    if (color == 'w') {
        printf("CLIENT IS WHITE\n");
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
    } else {
        printf("CLIENT IS BLACK\n");
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


/* constructMessage - Makes a message struct
 *   @params: data - Pointer to the beginning of the message data
 *            data_size - Size of the data (usually MAX_CHUNK_SIZE, unless
 *                        the whole data being sent will fit in one chunk).
 *            msg_type - Indicates the type of the data being sent (song, etc).
 *            index - Index in group of messages that comprise whole of data.
 *   @retval: struct msg* - Fully packed message.
 *
struct msg* constructMessage(char* data, int data_size, int msg_type,
                             int index) {

    // Making new message 
    struct msg* new_msg = malloc(sizeof(struct msg));
    new_msg->data = data;
    new_msg->data_size = min(data_size, MAX_CHUNK_SIZE);
    new_msg->amt_sent = 0;
    new_msg->type = msg_type;

    uint32_t x = htonl((uint32_t)(new_msg->data_size));
    memcpy(new_msg->header, &x, 4);

    x = htonl((uint32_t)(msg_type));
    memcpy(new_msg->header + 4, &x, 4);

    x = htonl((uint32_t)(index));
    memcpy(new_msg->header + 8, &x, 4);

    return new_msg;
}

*/
