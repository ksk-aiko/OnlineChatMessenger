import socket

class Client:
    def __init__(self, username, host, port):
        self.username = username
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def sendMessage(self, message):
        self.socket.send(message.encode())

    def receiveMessage(self):
        message = self.socket.recv(4096).decode()
        return message

    def close(self):
        self.socket.close()

def main():
    # CLIでユーザー名を入力
    username = input("Enter your username: ")
    host = input("Enter the server's IP address: ")
    port = int(input("Enter the server's port number: "))
    # クライアントインスタンスを作成。
    client = Client(username, host, port)    
    # サーバーに接続
    print("Connecting to the server...")
    client.connect()



if __name__ == "__main__":
    main()