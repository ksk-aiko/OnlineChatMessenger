import socket

class Client:
    def __init__(self, username, server_address, token=None):
        self.username = username
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.token = token
    
    def create_room(self, room_name, password):
        # TCP接続を確立
        self.tcp_socket.connect(self.server_address)
        # チャットルームの作成リクエストを送信
        self.tcp_socket.send(f"CREATE_ROOM {room_name} {password} {self.token}".encode())
        # サーバーからトークンを受信
        response_token = self.tcp_socket.recv(1024).decode()
        self.token = response_token
        # TCP接続を切断
        self.tcp_socket.close()

    def join_room(self, room_name, password):
        # TCP接続を確立
        self.tcp_socket.connect(self.server_address)
        # チャットルームの参加リクエストを送信
        self.tcp_socket.send(f"JOIN_ROOM {room_name} {password} {self.token}".encode())
        # サーバーからトークンを受信
        response = self.tcp_socket.recv(1024).decode()
        # TODO:joinの要求をサーバが受け入れた場合の、クライアント側の処理を追加する
        # TCP接続を切断
        self.tcp_socket.close()

    def send_message(self, message):
        # UDPでメッセージを送信
        self.udp_socket.sendto(f"{self.username}: {message}".encode(), self.server_address)

    def receive_message(self):
        # UDPでメッセージを受信
        message, address = self.udp_socket.recvfrom(1024)
        return message.decode()
    
    def close(self):
        self.udp_socket.close()

