import os
import sys
import socket

class Server:
    def __init__(self):
        self.ip = '0.0.0.0'
        self.port = 9001
        self.clients = []
        self.server = None

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.ip, self.port))
        print('Server started')
        
        while True:
            connection, client_address = self.server.accept()
            try:
                print('Connection from', client_address)
            except Exception as e:
                print(e)
                break
            finally:
                connection.close()
            
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