# Connection Establishment and FTP Command Learning Resource
# http://slacksite.com/other/ftp.html
# https://tools.ietf.org/html/rfc959

import socket

socket_cmd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

portCMD = 21
#portDATA = 20

socket_cmd.bind(('', portCMD))
#socket_data.bind(('', portDATA))

socket_cmd.listen(100)

#def send_data(data):
#    data += "\r\n"
#    data = data.encode()
#    data_conn.send()
#
#def recv_data(data):
#    data_conn.recv()

def send_cmd(data):
    data += "\r\n"
    data = data.encode()
    cmd_conn.send(data)
    print(data)

def recv_cmd():
    data = cmd_conn.recv(1024)
    print(data)
    return data.decode()

print("---> Server Socket Listening")

cmd_conn, cmd_addr = socket_cmd.accept()

print("--> Connected from", cmd_addr)

#port_data = cmd_addr[1] + 1

send_cmd("220 FTPproject v1.0")
username = recv_cmd()
send_cmd("331 Please specify the password.")
password = recv_cmd()
send_cmd("230 " + username + " Logged in.")

socket_cmd.close()
socket_data.close()
