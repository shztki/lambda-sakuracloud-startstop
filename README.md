# Lambda code for SAKURACLOUD Server Auto Start/Stop

## Description
特定のタグ `autostartstop` があるさくらのクラウドのサーバを起動/停止する Pythonスクリプトを lambda に登録し、CloudWatch Events でスケジュール実行するサンプル

## Requirements
* Terraform 0.12+
* Python 3.6+

## Environment variables
```
AWS_PROFILE
AWS_DEFAULT_REGION
TF_VAR_sacloud_access_token
TF_VAR_sacloud_access_token_secret
TF_VAR_slack_webhook_url
```
* `AWS_PROFILE` は `AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY` の 2つを指定するのと同義です。
* `TF_VAR_slack_webhook_url` は先頭の `https://` を除いたものです。

## Usage
```
git clone https://github.com/shztki/lambda-sakuracloud-startstop
cd lambda-sakuracloud-startstop/source
pip install -r requirements.txt -t lib
cp main.py lib/
cd ../
terraform init
terraform plan
terraform apply
```
* バックエンドはリモートにしています。ローカルで試す場合は main.tf の `backend "remote" {}` をコメントアウトしてください。
	* https://www.terraform.io/docs/backends/types/remote.html
	* https://learn.hashicorp.com/terraform/cloud-gettingstarted/tfc_signup

## Script Test
```
cd source/
pip install python-lambda-local
python-lambda-local --function lambda_handler --library lib --timeout 300 main.py event.json
```
```
# cat event.json
{
  "Action": "Start"
}
```
* スクリプトの動作をローカルで確認する方法のひとつです。
* 実際に指定した環境に対して実行されてしまうので注意。
* 3つの環境変数について、KMS で復号化する処理を入れているので、環境変数を参照するのみに変更する必要あり。


## Tags
|tag  |動作  |
|---|---|
|autostartstop  |起動・停止を実行  |

## Events
CloudWatchイベント側でスケジュールを作成し、`Action` として `Start / Stop` どちらかを指定

## Remark
* さくらのクラウドのサーバを業務時間外は停止しておきたい場合などに利用。
* 1台を起動するのに 30秒程度かかるため、lambda の timeout を 300秒より長くする必要がでてくる可能性あり。
