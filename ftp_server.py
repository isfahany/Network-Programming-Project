# Connection Establishment and FTP Command Learning Resource
# http://slacksite.com/other/ftp.html
# https://tools.ietf.org/html/rfc959
import socket
import threading

socket_cmd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
portCMD = 21
socket_cmd.bind(('', portCMD))
socket_cmd.listen(100)

def login(conn):
        send_cmd("220 FTPproject v1.0",conn)
        username = recv_cmd(conn)
        send_cmd("331 Please specify the password.",conn)
        password = recv_cmd(conn)
        send_cmd("230 " + username + " Logged in.",conn)



def conn_threading(conn):
    login(conn)

def send_cmd(data,conn):
    data += "\r\n"
    data = data.encode()
    conn.send(data)
    print(data)

def recv_cmd(conn):
    data = conn.recv(1024)
    print(data)
    return data.decode()

print("---> Server Socket Listening")

while True:
    cmd_conn, cmd_addr = socket_cmd.accept()
    print("---> Connected from", cmd_addr)
    connThread = threading.Thread(target=conn_threading, args=(cmd_conn,))
    connThread.start()

socket_cmd.close()
socket_data.close()
