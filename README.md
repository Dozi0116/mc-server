# mc-server
GCP上にあるマイクラサーバーをdiscordで管理するbot

## 使い方
環境変数に以下の項目を設定しておく。

- BOT_TOKEN : discord botのアクセストークン(ex. h0gEHoGEt0k3n)
- GCP_PROJECT : サーバーインスタンスがあるプロジェクト名(ex. my-mc-server)
- GCE_ZONE : サーバーインスタンスがあるゾーン名(ex. asia-northeast1-a)
- GCE_INSTANCE : サーバーインスタンス名(ex. mc-server)

以上の項目を設定した上でbot.pyを起動させる。

discord botもgcp上で動かすなら、startup-scriptにscreenを使った起動スクリプトを書くと良い。
