# Lambda code for SAKURACLOUD Server Auto Start/Stop

## Description
特定のタグ `autostartstop` があるさくらのクラウドのサーバを起動/停止する Pythonスクリプトを lambda に登録し、CloudWatchEvent で実行するサンプル

## Test Sample
テストといっても、実際に環境に対して実行されてしまうので注意
```
# cd source/
# pip install python-lambda-local
# pip install -r requirements.txt -t lib
# python-lambda-local --function lambda_handler --library lib --timeout 300 main.py event.json
```
```
# cat event.json
{
  "Action": "Start"
}
```

## Tags
|tag  |動作  |
|---|---|
|autostartstop  |起動・停止を実行  |

## Event
CloudWatchイベント側でスケジュールを作成し、`Action` として `Start / Stop` どちらかを指定

## Remark
* さくらのクラウドのサーバを業務時間外は停止しておきたい場合などに利用
* 1台を起動するのに 30秒程度かかるため、lambda の timeout を 300秒より長くする必要がでてくる可能性あり
