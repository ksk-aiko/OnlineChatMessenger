import socket
import threading

class Client:
    def __init__(self, username, server_address, token=None):
        self.username = username
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.token = token
        threading.Thread(target=self.receive_message).start()
    
    def create_room(self, room_name, password):
        try:
            # TCP接続を確立
            self.tcp_socket.connect(self.server_address)
            # チャットルームの作成リクエストを送信
            self.tcp_socket.send(f"CREATE_ROOM {self.username} {room_name} {password} {self.token}".encode())
            # サーバーからトークンを受信
            response_token = self.tcp_socket.recv(1024).decode()
            self.token = response_token
            print('you are successfully created a room!')
        except Exception as e:
            print(f"An error occurred while creating the room: {e}")
        finally:
            # TCP接続を切断
            self.tcp_socket.close()
    def join_room(self, room_name, password):
        try:
            # TCP接続を確立
            self.tcp_socket.connect(self.server_address)
            # チャットルームの参加リクエストを送信
            self.tcp_socket.send(f"JOIN_ROOM {room_name} {password} {self.token}".encode())
            # サーバーからレスポンスを受信
            response = self.tcp_socket.recv(1024).decode()
            if response == "OK":
                print("Successfully joined the room")
            else:
                print("Failed to join the room")
        except Exception as e:
            print(f"An error occurred while joining the room: {e}")
        finally:
            # TCP接続を切断
            self.tcp_socket.close()
    
    # UDPで接続
    def connect_udp(self):
        self.server_address = (self.server_address[0], 9001)
        self.udp_socket.connect(self.server_address)

    def send_message(self, message):
        try:
            # UDPでメッセージを送信
            self.server_address = (self.server_address[0], 9001)
            print(f"Sended message to: {self.server_address}")
            self.udp_socket.sendto(f"{self.username} {message}".encode(), self.server_address)
            print(f"send_message() is successfully executed, sended data -> {self.username} {message} {self.server_address}")
        except Exception as e:
            print(f"An error occurred while sending the message: {e}")

    def receive_message(self):
        try:
            # UDPでメッセージを受信
            data, address = self.udp_socket.recvfrom(1024)
            message = data.decode()
            print(f"Received message: {message} from {address}")
        except Exception as e:
            print(f"An error occurred while receiving the message: {e}")
    
    def close(self):
        self.udp_socket.close()

def main():
    print("Enter your username:")
    username = input()
    print("Are you a new user? (yes/no)")
    user_response = input()
    if user_response == "yes":
        print("Enter the server IP address:")
        print("Omit the input this time.")
        ip = '0.0.0.0'
        print("Do you create a new room or join an existing room? (create/join)")
        room_response = input()
        if room_response == "create":
            print("Enter the room name:")
            room_name = input()
            print("Enter the room password:")
            password = input()
            client = Client(username, (ip, 9002))
            client.create_room(room_name, password)
            print('Enter your first message:')
            first_message = input()
            client.send_message(first_message)
        elif room_response == "join":
            try:
                print("Enter the room name:")
                room_name = input()
                print("Enter the room password:")
                password = input()
                print("Enter the token:")
                token = input().strip()
                print('ok, wait...')
                client = Client(username, (ip, 9002), token)
                print('for debug')
                client.join_room(room_name, password)
                print('for debug2')
            except Exception as e:
                print(f"An error occurred while joining the room: {e}")
        else:
            print('Invalid command')
        
        while True:
            print("Enter a message:")
            message = input()
            client.send_message(message)
            client.receive_message()

if __name__ == "__main__":
    main()