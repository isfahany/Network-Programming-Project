# Connection Establishment and FTP Command Learning Resource
# http://slacksite.com/other/ftp.html
# https://tools.ietf.org/html/rfc959
import socket
import threading
import os
import sys
import hashlib

socket_cmd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
portCMD = 21
socket_cmd.bind(('', portCMD))
socket_cmd.listen(100)

commandlist = ["USER", "QUIT", "PORT", "TYPE", "MODE", "STRU", "RETR", "STOR",
              "NOOP", "LIST", "SYST"]


def QUIT(conn):
    send_cmd("221 Goodbye.\r\n", conn)

def ex421(conn):
    send_cmd("421 Command not working", conn)

def SYST(conn):
    try:
        send_cmd("215 " + os.uname()[0] + " " + os.uname()[-1], conn)
    except:
        ex421(conn)

def NOOP(conn):
    conn.send("200 Keep Alived.\r\n", conn)

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

def RETR(conn, file_up, data_addr, data_port):
    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock.connect((data_addr, data_port))
    files = open(file_up, "rb")
    data = files.read()
    send_cmd("150 Opening Download data connection", conn)
    data_sock.send(data)
    data_sock.close()
    send_cmd("226 Completed", conn)

def PORT(conn, command):
    try:
        data = command[5:].split(",")
        data_addr = ".".join(data[:4])
        data_port = (int(data[4])<<8) + int(data[5])
        send_cmd("200 PORT command successful. Consider using PASV.", conn)
    except:
        ex421(conn)
    return data_addr, data_port

def PWD(conn):
    path = os.getcwd()
    send_cmd("257 "+ path, conn)

def CDUP(conn):
    os.chdir("..")
    send_cmd("200 OK.",conn)

def encrypt_string(hash_string):
    enc = hashlib.sha256(hash_string.encode()).hexdigest()
    return enc

def login(conn):
    send_cmd("220 FTPproject v1.0", conn)
    username = recv_cmd(conn)
    send_cmd("331 Please specify the password.", conn)
    password = recv_cmd(conn)
    user = username.split()
    user = str(user[1])
    password = password.split()
    password = encrypt_string(str(password[1]))
    for line in open("accountfile.txt","r").readlines(): # Read the lines
        account_info = line.split()
        if user == account_info[0] and password == account_info[1]:
            print("Correct credentials!")
            send_cmd("230 User " + username + " Logged in.", conn)
            break
        else:
            send_cmd("230 User anonymous", conn)
            break

def conn_threading(conn):
    login(conn)
    while True:
        command = recv_cmd(conn)
        print(command)
        if "SYST" in command:
            print("syst is not available")
            #SYST(conn)
        elif "QUIT" in command:
            sys.exit()
        elif "PORT" in command:
            data_addr, data_port = PORT(conn, command)
        elif "LIST" in command:
            LIST(conn, data_addr, data_port)
        elif "CDUP" in command:
            CDUP(conn)
        elif "PWD" in command:
            PWD(conn)
        elif "QUIT" in command:
            QUIT(conn)
        elif "NOOP" in command:
            NOOP(conn)
        elif "RETR" in command:
            file_up = command[5:-2]
            RETR(conn, file_up, data_addr, data_port)
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
