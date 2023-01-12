# C0A20128 疋田辰起の創生課題
## 提案ソフトウェア
alert_softに今回制作したソフトウェアがあります．

対象のマイクロサービスに対してのアラートを設定するソフトウェアです．


### 必要なもの
`istioctl dashboard`で立ち上げた`Jaeger`と`Prometheus`のURL

slack_webhook用のURL

対象のマイクロサービスのポート番号

これらを入力し，`main.py`を実行します．

## 負荷試験
locustfile.pyは今回使用したlocustのテストシナリオです．

`locust -h localhost -f locustfile.py`で実行します．
