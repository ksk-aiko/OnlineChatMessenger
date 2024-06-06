import os
import sys
import socket

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
        print(f"Server started at {self.ip}:{self.udp_port} and {self.ip}:{self.tcp_port}")
        while True:
            try:
                self.handle_tcp_connection()
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def handle_tcp_connection(self):
        conn, addr = self.tcp_socket.accept()
        print(f"Connection from {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode()
            print(f"Received: {data}")
            response = self.handle_tcp_request(data)
            conn.send(response.encode())
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
            if room_name in self.chat_rooms and self.chat_rooms[room_name] == password:
                self.tokens[token] = room_name
                return "OK"
            else:
                return "ERROR"
        else:
            return "ERROR"


