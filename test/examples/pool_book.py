import socket
from time import sleep
import booktest as bt


PORT_RANGE = bt.port_range(10000, 10002)


def t_open_server_socket(t: bt.TestCaseRun, port):
    server_socket = \
        t.t(f" * creating server socket..").imsln(
            lambda: socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    try:
        # Bind the socket to the specified port
        t.t(f" * binding the socket in port ").i(f"{port}..").imsln(
            lambda: server_socket.bind(('localhost', port)))
        # Start listening for connections
        t.t(f" * start listening to the connection..").imsln(
            lambda: server_socket.listen(1))
        t.t(" * server socket opened at port ").iln(f"{port}")

        # Keep the socket open for 300 milliseconds
        t.t(" * sleeping for 100 milliseconds..").imsln(
            lambda: sleep(0.1))
    finally:
        # Close the socket
        server_socket.close()
        t.t(" * server socket closed at port ").iln(f"{port}.")


@bt.depends_on(PORT_RANGE)
def test_port_pool_1(t: bt.TestCaseRun, port):
    t_open_server_socket(t, port)


@bt.depends_on(PORT_RANGE)
def test_port_pool_2(t: bt.TestCaseRun, port):
    t_open_server_socket(t, port)


@bt.depends_on(PORT_RANGE)
def test_port_pool_3(t: bt.TestCaseRun, port):
    t_open_server_socket(t, port)


@bt.depends_on(PORT_RANGE)
def test_port_pool_4(t: bt.TestCaseRun, port):
    t_open_server_socket(t, port)
