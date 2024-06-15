import os
import socket
import threading

class Server:
    def __init__(self):
        self.ip = '0.0.0.0'
        self.udp_port = 9001
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_port = 9002
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_rooms = {}
        self.tokens = {}

    def start(self):
        self.udp_socket.bind((self.ip, self.udp_port))
        self.tcp_socket.bind((self.ip, self.tcp_port))
        self.tcp_socket.listen(5)
        print(f"Server started at UDP -> {self.ip}:{self.udp_port} and TCP -> {self.ip}:{self.tcp_port}")
        while True:
            try:
                conn, addr = self.tcp_socket.accept()
                threading.Thread(target=self.handle_tcp_connection, args=(conn, addr)).start()
                # UDPでの接続を処理
                data, addr = self.udp_socket.recvfrom(1024)
                threading.Thread(target=self.handle_udp_connection, args=(data, addr)).start()
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
                response = self.handle_tcp_request(data)
                print(response)
                conn.send(response.encode())
                print('sent response to client')
            except Exception as e:
                print(f"An error occurred: {e}")
                break
        conn.close()

    def generate_token(self):
        return os.urandom(16).hex()
    
    def handle_tcp_request(self, data):
        parts = data.split()
        if parts[0] == "CREATE_ROOM":
            room_name, password = parts[1], parts[2]
            token = self.generate_token()
            self.chat_rooms[room_name] = password
            self.tokens[token] = room_name
            return token
        elif parts[0] == "JOIN_ROOM":
            room_name, password, token = parts[1], parts[2], parts[3]
            if room_name in self.chat_rooms and self.chat_rooms[room_name] == password and self.tokens[token] == room_name:
                return "OK"
            else:
                return "ERROR"
        else:
            return "ERROR"
    
    def handle_udp_connection(self, data, addr):
        print(f"Received UDP data: {data} from {addr}")
        print('Sends a successful receipt message to the client.')
        self.udp_socket.sendto("OK".encode(), addr)

def main():
    server = Server()
    server.start()

if __name__ == "__main__":
    main()

