/*
    This program provides an example of interfacing with
    libmyolinux. A packet of raw data is passed in, interpreted
    as a Myo Armband packet, and data is returned.

*/

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include "myolinux.h"

int main(){
	unsigned char buffer[30];

	struct sockaddr_in server;
	memset(&server, 0, sizeof(struct sockaddr_in));
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = htonl(INADDR_ANY);
	server.sin_port = htons(6969);

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    bind(sock, (struct sockaddr *) &server, sizeof(server));

    listen(sock, 10);
    int conn = accept(sock, (struct sockaddr *) NULL, NULL);

    while (1) {
    	recv(conn, buffer, 30, 0);
    	parse_gesture(buffer);
    }

    close(conn);
    close(sock);

    /* Real sample packet */
    // unsigned char data[30] = {0x0,0x0,0xc2,0xbd,0x0,0x0,0x48,0x3c,0x0,0x80,0x71,0x3f,0x0,0x4c,0x0d,0xbf,0x0,0x40,0xbd,0x0,0x20,0x9a,0xbd,0x0,0x6c,0x54,0x3f,0xff,0x01,0x0};

    // parse_packet(data);

    return 0;
}
