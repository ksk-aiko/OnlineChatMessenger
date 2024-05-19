import socket

class Client:
    def __init__(self, username, host, port):
        self.username = username
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self):
        print("Connecting to the server...")
        try:
            self.socket.connect((self.host, self.port))
            print("Connected to the server")
        except Exception as e:
            print("Error connecting to the server:", str(e))

    def sendMessage(self, message):
        try:
            self.socket.send(message.encode())
        except Exception as e:
            print("Error sending message:", str(e))

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
    client.connect()
    # メッセージを送信
    message = input("Enter a message: ")
    client.sendMessage(message)
    



if __name__ == "__main__":
    main()