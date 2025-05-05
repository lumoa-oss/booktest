import socket
from time import sleep
import booktest as bt


PORT_POOL = bt.port_range(10000, 10002)


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


def t_open_two_server_sockets(t: bt.TestCaseRun, port, port2):
    server_socket = \
        t.t(f" * creating server socket..").imsln(
            lambda: socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    server_socket2 = \
        t.t(f" * creating server socket 2..").imsln(
            lambda: socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    try:
        # Bind the socket to the specified port
        t.t(f" * binding the socket in port ").i(f"{port}..").imsln(
            lambda: server_socket.bind(('localhost', port)))

        t.t(f" * binding the socket 2 in port ").i(f"{port2}..").imsln(
            lambda: server_socket2.bind(('localhost', port2)))

        # Start listening for connections
        t.t(f" * start listening to the connection..").imsln(
            lambda: server_socket.listen(1))
        t.t(" * server socket opened at port ").iln(f"{port}")

        # Start listening for connections
        t.t(f" * start listening to the connection..").imsln(
            lambda: server_socket2.listen(1))
        t.t(" * server socket 2 opened at port ").iln(f"{port2}")

        # Keep the socket open for 300 milliseconds
        t.t(" * sleeping for 100 milliseconds..").imsln(
            lambda: sleep(0.1))
    finally:
        # Close the socket
        server_socket.close()
        t.t(" * server socket closed at port ").iln(f"{port}.")

        # Close the socket
        server_socket2.close()
        t.t(" * server socket 2 closed at port ").iln(f"{port2}.")



@bt.depends_on(PORT_POOL)
def test_port_pool_1(t: bt.TestCaseRun, port):
    t_open_server_socket(t, port)

@bt.depends_on(PORT_POOL, PORT_POOL)
def test_port_pool_with_2_ports(t: bt.TestCaseRun, port, port2):
    t_open_two_server_sockets(t, port, port2)

@bt.depends_on(PORT_POOL)
def test_port_pool_2(t: bt.TestCaseRun, port):
    t_open_server_socket(t, port)

@bt.depends_on(PORT_POOL, PORT_POOL)
def test_port_pool_with_2_ports_2(t: bt.TestCaseRun, port, port2):
    t_open_two_server_sockets(t, port, port2)

@bt.depends_on(PORT_POOL)
def test_port_pool_3(t: bt.TestCaseRun, port):
    t_open_server_socket(t, port)

