import os
import sys
import socket

class Server:
    def __init__(self):
        self.ip = '0.0.0.0'
        self.port = 9001
        self.clients = []
        self.server = None

    def receiveMessage(self):
        data, addr = self.server.recvfrom(4096)
        usernamelen = int(data[:2])
        print(usernamelen)

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.settimeout(30)
        self.server.bind((self.ip, self.port))
        print('Server started')
        
        while True:
            data, client_address = self.server.recvfrom(4096)
            try:
                print('Connection from', client_address)
                print('Received', data)
                # TODO:usernamelenを取得するコードを追加
            except Exception as e:
                print(e)
                break
            finally:
                print('Closing connection...')
                self.server.close()
                break

def main():
    server = Server()
    server.start()
    
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