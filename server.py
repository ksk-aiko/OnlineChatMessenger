import os
import sys
import socket
from datetime import datetime
import threading
import time

class Server:
    def __init__(self):
        self.ip = '0.0.0.0'
        self.port = 9001
        self.clients = {}
        self.server = None
        self.relaySystem = RelaySystem()
        self.running = True

    def addClient(self, client):
        self.clients[client] = ''
        print('Added client', client)
    
    def relayMessage(self, username, message):
        for client in self.clients:
            if client != username:
                # ユーザー名の長さをバイト列に変換
                usernamelen = len(username).to_bytes(1, 'big')
                # usernamelenとmessageを結合してサーバーに送信
                self.server.sendto(usernamelen + username.encode() + message.encode(), self.clients[client])
                print('Relayed message to', client)

    def receiveMessage(self):
        while self.running:
            try:
                data, client_address = self.server.recvfrom(4096)
                print('Connection from', client_address)
                print('Received', data)
                # ユーザー名の長さを取得
                usernamelen = int.from_bytes(data[:1], 'big')
                # ユーザー名を取得
                username = data[1:1+usernamelen].decode()
                # メッセージを取得
                message = data[1+usernamelen:].decode()

                print('Received message from', username, ':', message)

                if username not in self.clients:
                    self.addClient(username)
                
                self.relaySystem.clientInfo[username] = message + ' | ' + str(datetime.now())
                print(self.relaySystem.clientInfo)

                self.relayMessage(username, message)


            except Exception as e:
                print(e)

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.settimeout(30)
        self.server.bind((self.ip, self.port))
        print('Server started')

        receive_thread = threading.Thread(target=self.receiveMessage)

        receive_thread.start()

        receive_thread.join()

    def stop(self):
        self.running = False
        print('Stopping server...')
        self.server.close()
        sys.exit()

class RelaySystem:
    def __init__(self):
        self.clientInfo = {}

def main():
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

if __name__ == "__main__":
    main()

# import socket


# class UDPSocket:
#     # IPアドレスとポート番号を指定してソケットを作成する。インスタンス生成時にbindも行う。
#     def __init__(self, ip, port):
#         self.ip = ip
#         self.port = port
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.socket.bind((self.ip, self.port))

#     def sendData(self, data):
#         # dataはバイト列である必要がある
#         self.socket.sendto(data, (self.ip, self.port))
        
#     def receiveData(self):
#         data, addr = self.socket.recvfrom(4096)
#         return data, addr