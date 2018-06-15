import socket
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = 'localhost'
# port = 8000
#
# def connect(host, port):
#     sock.connect((host, port))
#
# def mysend():
#     totalsent = 0
#     sock.send(b'stop')
#
# def receive():
#     print(sock.recv(2048))
#
# connect(host,port)
# receive()
# mysend()
# 22, 445, 548, 631
# print(socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(('192.168.200.116',22)))
"""mac = [22, 445, 548, 631]
linux = [20, 21, 22, 23, 25, 80, 111, 443, 445, 631, 993, 995]
windows = [135, 137, 138, 139, 445]
"""
x ='192.168.0.10'


def prr(x):
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex((x, 22))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.setblocking(0)
    socket.setdefaulttimeout(1)

    try:
        _socker = sock.connect_ex((x, 8000))
        if _socker == 0:
            print('Found online at {}'.format(x))
        else:
            print('{} responded {}'.format(x, _socker))
    except PermissionError:
        print('permission')
    except ConnectionRefusedError:
        print('Refused')
    finally:
        sock.close()
    # print('Connection returned {} for {}'.format(_socker, x))

for _subnet in range(0, 15):
    print(_subnet)
    adde = '192.168.0.{}'.format(_subnet)
    prr(adde)
#
#     network = '192.168.200.1{}'.format(_subnet)
#     print(network)
#     if _subnet == 16:
#         network = 'localhost'.format(_subnet)
#     socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     socket.setdefaulttimeout(1)
#     result = socket_obj.connect((network,8000))
#     print(result)
#     if result == 0:
#         # Logger.info('Found online at {}'.format(network))
#         print('Found online at {}'.format(network))
#
#         # Logger.info('Host name {}'.format(socket.gethostname()))
#         print('Host name {}'.format(socket.gethostname()))
#         _url.append('{}'.format(network))

    # else:
    #     socket_obj.close()
    # Logger.info('Current :{} Exiting'.format(threading.currentThread().getName()))