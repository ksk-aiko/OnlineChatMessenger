# タスクリスト

## コーディング

### クライアントクラスの実装
- [x] `Client` クラスの作成
  - [x] コンストラクタの実装
    - [x] ユーザー名、TCPソケット、UDPソケット、サーバーアドレス、トークンの初期化
  - [x] `create_room` メソッドの実装
    - [x] TCP接続を確立
    - [x] チャットルーム作成要求をサーバーに送信
    - [x] サーバーからトークンを受信
    - [x] TCP接続を閉じる
  - [x] `join_room` メソッドの実装
    - [x] TCP接続を確立
    - [x] チャットルーム参加要求をサーバーに送信
    - [x] サーバーからトークンを受信
    - [x] TCP接続を閉じる
  - [x] `send_message` メソッドの実装
    - [x] トークンを含むメッセージをUDPで送信
  - [x] `receive_message` メソッドの実装
    - [x] UDPでメッセージを受信し表示
  - [x] `close` メソッドの実装
    - [x] UDPソケットを閉じる

### サーバークラスの実装
- [ ] `Server` クラスの作成
  - [x] コンストラクタの実装
    - [x] TCPソケット、UDPソケットの初期化
    - [x] チャットルームとトークンの管理用データ構造の初期化
  - [ ] `start` メソッドの実装
    - [ ] TCPおよびUDPソケットを開始
    - [ ] TCP接続処理スレッドの起動
    - [ ] UDPメッセージ処理スレッドの起動
  - [ ] `handle_tcp_connections` メソッドの実装
    - [ ] クライアントからのTCP接続を受け入れ
    - [ ] 各クライアント接続に対して新しいスレッドを起動
  - [ ] `handle_client` メソッドの実装
    - [ ] クライアントからのデータを受信
    - [ ] チャットルーム作成要求または参加要求を処理
    - [ ] トークンを生成しクライアントに送信
    - [ ] TCP接続を閉じる
  - [ ] `handle_udp_messages` メソッドの実装
    - [ ] UDPメッセージを受信
    - [ ] トークンを検証しメッセージをリレー
  - [ ] `generate_token` メソッドの実装
    - [ ] 一意のトークンを生成

### 補助クラスの実装
- [ ] `RelaySystem` クラスの作成
  - [ ] コンストラクタの実装
    - [ ] クライアント情報の管理用データ構造の初期化
  - [ ] クライアント情報の管理メソッドの実装
    - [ ] クライアント情報の追加、削除、更新メソッドの実装