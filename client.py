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
            # ユーザー名の長さをバイト列に変換
            usernamelen = len(self.username).to_bytes(1, 'big')
            # usernamelenとmessageを結合してサーバーに送信
            self.socket.send(usernamelen + self.username.encode() + message.encode())
        except Exception as e:
            print("Error sending message:", str(e))

    def receiveMessage(self):
        try:
            data = self.socket.recv(4096)
            # ユーザー名の長さを取得
            usernamelen = int.from_bytes(data[:1], 'big')
            # ユーザー名を取得
            username = data[1:1+usernamelen].decode()
            # メッセージを取得
            message = data[1+usernamelen:].decode()
            print('Received message from', username, ':', message)
        except Exception as e:
            print("Error receiving message:", str(e))
            

    def close(self):
        self.socket.close()

def main():
    while True:
        # CLIでユーザー名を入力
        username = input("Enter your username: ")
        # host = input("Enter the server's IP address: ")
        host = '0.0.0.0'
        # port = int(input("Enter the server's port number: "))
        port = 9001
        # クライアントインスタンスを作成。
        client = Client(username, host, port)    
        # サーバーに接続
        client.connect()
        # メッセージを送信
        message = input("Enter a message: ")
        client.sendMessage(message)
        client.receiveMessage()




if __name__ == "__main__":
    main()