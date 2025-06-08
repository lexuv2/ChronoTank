#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>

#ifndef CLOCK_MONOTONIC
#define CLOCK_MONOTONIC 1
#endif

#define PORT 12345
#define BUFSIZE 128

int main() {
    int sock = 0;
    struct sockaddr_in serv_addr;
    char buffer[BUFSIZE] = {0};
    struct timespec start, end;

#if defined(CLOCK_MONOTONIC_RAW)
    #define MY_CLOCK CLOCK_MONOTONIC_RAW
#else
    #define MY_CLOCK CLOCK_MONOTONIC
#endif

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("Socket creation error");
        return 1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
        perror("Invalid address/ Address not supported");
        return 1;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connection Failed");
        return 1;
    }

    // printf("Enter password: ");
    if (fgets(buffer, BUFSIZE, stdin) == NULL) {
        printf("Input error\n");
        close(sock);
        return 1;
    }
    // Remove trailing newline
    buffer[strcspn(buffer, "\n")] = 0;

    clock_gettime(MY_CLOCK, &start);
    send(sock, buffer, strlen(buffer), 0);

    int valread = read(sock, buffer, BUFSIZE - 1);
    clock_gettime(MY_CLOCK, &end);

    if (valread > 0) {
        buffer[valread] = '\0';
        printf("%s", buffer);
    }

    long seconds = end.tv_sec - start.tv_sec;
    long nanoseconds = end.tv_nsec - start.tv_nsec;
    double elapsed = seconds + nanoseconds*1e-9;
    printf("%.9f\n", elapsed);

    close(sock);
    return 0;
}
