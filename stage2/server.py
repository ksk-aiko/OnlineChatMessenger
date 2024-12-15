import os
import socket
import threading
# datetimeモジュールをインポート
from datetime import datetime

class Server:
    def __init__(self):
        self.ip = '0.0.0.0'
        self.udp_port = 9001
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_port = 9002
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_rooms = {}
        self.tokens = {}
        self.relaySystem = RelaySystem()
        self.udp_socket.bind((self.ip, self.udp_port))
        self.tcp_socket.bind((self.ip, self.tcp_port))
        self.tcp_socket.listen(5)
        self.running = True

    def addClient(self, client):
        self.relaySystem.clientInfo[client] = ''
        print('Added client', client)
    
    def relayMessage(self, username, message):
        #TODO: 2人目のクライアントのメッセージが1人目クライアントにリレーされない問題を解決する
        print(f'Now, we hava these clients -> {self.relaySystem.clientInfo}')
        for client in self.relaySystem.clientInfo:
            if client != username:
                self.udp_socket.sendto(f'From {username}: {message}'.encode(), self.relaySystem.clientInfo[client])
                print('Relayed message to', client)
            else:
                #self.udp_socket.sendto(b'OK', self.relaySystem.clientInfo[username])
                continue
    def start(self):
        print(f"Server started at UDP -> {self.ip}:{self.udp_port} and TCP -> {self.ip}:{self.tcp_port}")
        while True:
            try:
                conn, addr = self.tcp_socket.accept()
                threading.Thread(target=self.handle_tcp_connection, args=(conn, addr)).start()
                # UDPでの接続を処理
                data, addr = self.udp_socket.recvfrom(1024)
                threading.Thread(target=self.handle_udp_connection, args=(data, addr)).start()
                # threading.Thread(target=self.receiveMessage).start()
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def handle_tcp_connection(self, conn, addr):
        print(f"Connection from {addr}")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                data = data.decode()
                print(f"Received: {data}")
                generated_token = self.handle_tcp_request(data)
                print(f'Genereated token is {generated_token}')
                conn.send(generated_token.encode())
                print('Sended token to client.')
            except Exception as e:
                print(f"An error occurred: {e}")
                break
        conn.close()

    def generate_token(self):
        return os.urandom(16).hex()
    
    def handle_tcp_request(self, data):
        parts = data.split()
        if parts[0] == "CREATE_ROOM":
            client, room_name, password = parts[1], parts[2], parts[3]
            token = self.generate_token()
            self.chat_rooms[room_name] = password
            self.tokens[token] = room_name
            self.addClient(client)
            return token
        elif parts[0] == "JOIN_ROOM":
            client_name, room_name, password, token = parts[1], parts[2], parts[3], parts[4]
            if room_name in self.chat_rooms and self.chat_rooms[room_name] == password and self.tokens[token] == room_name:
                self.addClient(client_name)
                return "OK"
            else:
                return "ERROR"
        else:
            return "ERROR"
    
    def handle_udp_connection(self, data, addr):
        print(f"Received UDP data: {data} from {addr}")
        client_name = data.decode().split()[0]
        message = data.decode()[len(client_name)+1:]
        print('Sends a successful receipt message to the client.')
        self.udp_socket.sendto(f"OK -> Server received data successfully from {client_name}".encode(), addr)
        if self.relaySystem.clientInfo[client_name] == '':
            self.relaySystem.clientInfo[client_name] = addr
            self.relayMessage(client_name, message)
        self.receiveMessage()
    
    def receiveMessage(self):
        print('Waiting  messages from client...')
        while self.running:
            try:
                data, client_address = self.udp_socket.recvfrom(4096)
                print('Connection from', client_address)
                print('Received', data)

                username = data.decode().split()[0]
                message = data.decode()[len(username)+1:]
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                print('Received message from', username, ':', message, ':', date)

                if username not in self.relaySystem.clientInfo:
                    self.addClient(username)
                
                self.relaySystem.clientInfo[username] = client_address
                self.relaySystem.clientMessage[username] = message
                self.relaySystem.clientLatestMessageDate[username] = date
                print(self.relaySystem.clientInfo)
                print(self.relaySystem.clientMessage)
                print(self.relaySystem.clientLatestMessageDate)

                # self.removeClientFromRelaySystem()
                self.relayMessage(username, message)

                # クライアントにメッセージを送信
                self.udp_socket.sendto(f'OK -> Server received data successfully. username: {username} message: {message}'.encode(), client_address)


            except Exception as e:
                print(e)

    def removeClientFromRelaySystem(self):
        for username in self.relaySystem.clientLatestMessageDate:
            if (datetime.now() - datetime.strptime(self.relaySystem.clientLatestMessageDate[username], '%Y-%m-%d %H:%M:%S')).seconds > 90:
                print('Removing client', username)
                del self.relaySystem.clientInfo[username]
                del self.relaySystem.clientMessage[username]
                del self.relaySystem.clientLatestMessageDate[username]
                print(self.relaySystem.clientInfo)
                print(self.relaySystem.clientMessage)
                print(self.relaySystem.clientLatestMessageDate)

class RelaySystem:
    def __init__(self):
        self.clientInfo = {}
        self.clientMessage = {}
        self.clientLatestMessageDate = {}

def main():
    server = Server()
    server.start()

if __name__ == "__main__":
    main()

