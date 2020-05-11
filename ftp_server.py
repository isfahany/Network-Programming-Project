# Connection Establishment and FTP Command Learning Resource
# http://slacksite.com/other/ftp.html
# https://tools.ietf.org/html/rfc959
import socket
import threading
import os
import sys

socket_cmd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
portCMD = 21
socket_cmd.bind(('', portCMD))
socket_cmd.listen(100)

commandlist = ["USER", "QUIT", "PORT", "TYPE", "MODE", "STRU", "RETR", "STOR",
              "NOOP", "LIST", "SYST"]



def ex421(conn):
    send_cmd("421 Command not working", conn)

def SYST(conn):
    try:
        send_cmd("215 " + os.uname()[0] + " " + os.uname()[-1], conn)
    except:
        ex421(conn)


def LIST(conn, data_addr, data_port):
    try:
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_sock.connect((data_addr, data_port))
        ls = os.listdir(".")
        send_cmd("150 Here comes the directory listing.\n", conn)
        print(ls)
        item = ""
        for i in ls:
            item += i + "\r\n"
        item = item[:-2]
        item = item.encode()
        data_sock.send(item)
        data_sock.close()
    except:
        ex421(conn)

def PORT(conn, command):
    try:
        data = command[5:].split(",")
        data_addr = ".".join(data[:4])
        data_port = (int(data[4])<<8) + int(data[5])
        send_cmd("200 PORT command successful. Consider using PASV.", conn)
    except:
        ex421(conn)
    return data_addr, data_port

def login(conn):
    send_cmd("220 FTPproject v1.0", conn)
    username = recv_cmd(conn)
    send_cmd("331 Please specify the password.", conn)
    password = recv_cmd(conn)
    send_cmd("230 User " + username + " Logged in.", conn)
    SYSTcomm = recv_cmd(conn)

def conn_threading(conn):
    login(conn)
    while True:
        command = recv_cmd(conn)
        print(command)
        if command == "SYST":
            SYST(conn)
        elif command == "QUIT":
            sys.exit()
        elif command == "LIST":
            LIST(conn)
        elif "PORT" in command:
            data_addr, data_port = PORT(conn, command)
        elif "LIST" in command:
            LIST(conn, data_addr, data_port)
        else:
            ex421(conn)
            continue

def send_cmd(data, conn):
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
