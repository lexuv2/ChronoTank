// Raw TCP communication version of sender2.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>
#include <linux/errqueue.h>
#include <linux/net_tstamp.h>
#include <errno.h>

void exit_error(const char *msg) {
    perror(msg);
    exit(EXIT_FAILURE);
}

long long timespec_diff(struct timespec *start, struct timespec *end) {
    long long sec = (long long)end->tv_sec - (long long)start->tv_sec;
    long long nsec = (long long)end->tv_nsec - (long long)start->tv_nsec;
    return sec * 1000000000LL + nsec;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <server_ip> <server_port> \"<raw_data>\"\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    const char *server_ip = argv[1];
    int server_port = atoi(argv[2]);
    const char *raw_data = argv[3];

    if (server_port <= 0 || server_port > 65535) {
        fprintf(stderr, "Invalid port number: %d\n", server_port);
        exit(EXIT_FAILURE);
    }

    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0)
        exit_error("socket");

    // Enable timestamping
    int flags = SOF_TIMESTAMPING_TX_SOFTWARE | 
                SOF_TIMESTAMPING_RX_SOFTWARE |
                SOF_TIMESTAMPING_SOFTWARE;
    if (setsockopt(sockfd, SOL_SOCKET, SO_TIMESTAMPING, &flags, sizeof(flags)))
        exit_error("setsockopt");

    struct sockaddr_in server_addr = {
        .sin_family = AF_INET,
        .sin_port = htons(server_port)
    };
    if (inet_pton(AF_INET, server_ip, &server_addr.sin_addr) <= 0)
        exit_error("inet_pton");

    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)))
        exit_error("connect");

    // Send raw TCP data
    ssize_t sent = send(sockfd, raw_data, strlen(raw_data), 0);
    if (sent != strlen(raw_data))
        exit_error("send");

    // Get TX timestamp from error queue
    struct msghdr msg = {0};
    struct iovec iov;
    char buf[512];
    char ctrl_buf[1024];
    struct timespec tx_time;

    iov.iov_base = buf;
    iov.iov_len = sizeof(buf);
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;
    msg.msg_control = ctrl_buf;
    msg.msg_controllen = sizeof(ctrl_buf);

    ssize_t n = recvmsg(sockfd, &msg, MSG_ERRQUEUE);
    if (n < 0)
        exit_error("recvmsg (tx)");

    // Extract TX timestamp
    struct cmsghdr *cmsg;
    for (cmsg = CMSG_FIRSTHDR(&msg); cmsg; cmsg = CMSG_NXTHDR(&msg, cmsg)) {
        if (cmsg->cmsg_level == SOL_SOCKET && 
            cmsg->cmsg_type == SCM_TIMESTAMPING) {
            struct timespec *times = (struct timespec *)CMSG_DATA(cmsg);
            tx_time = times[0]; // Use software timestamp
            break;
        }
    }

    // Receive response and get RX timestamp
    struct timespec rx_time;
    memset(&msg, 0, sizeof(msg));
    iov.iov_base = buf;
    iov.iov_len = sizeof(buf);
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;
    msg.msg_control = ctrl_buf;
    msg.msg_controllen = sizeof(ctrl_buf);

    n = recvmsg(sockfd, &msg, 0);
    if (n < 0)
        exit_error("recvmsg (rx)");

    // Extract RX timestamp
    for (cmsg = CMSG_FIRSTHDR(&msg); cmsg; cmsg = CMSG_NXTHDR(&msg, cmsg)) {
        if (cmsg->cmsg_level == SOL_SOCKET && 
            cmsg->cmsg_type == SCM_TIMESTAMPING) {
            struct timespec *times = (struct timespec *)CMSG_DATA(cmsg);
            rx_time = times[0]; // Use software timestamp
            break;
        }
    }

    // Print received data
    if (n > 0) {
        fwrite(buf, 1, n, stdout);
        if (buf[n-1] != '\n') putchar('\n');
    }

    // Calculate and print duration
    long long elapsed_ns = timespec_diff(&tx_time, &rx_time);
    printf("Request-Response time: %lld ns\n", elapsed_ns);
    printf("Raw TCP request fulfilled successfully.\n");

    close(sockfd);
    return 0;
}
