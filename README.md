#ALICE Batch

Pixivのデータ取得ツール


#インストールモジュール

```
pip3 install pixivpy
pip3 install PyMySQL
```

## 準備

sqlフォルダを参照

```
mysql anime_admin_development < sql/DDL/pixiv_tag_daily.sql
mysql anime_admin_development < sql/DDL/pixiv_tag_hourly.sql
mysql anime_admin_development < sql/DDL/pixiv_tag_status.sql
```

## 実行

```
python3 alice.py

デイリーで履歴を保存したい時
python3 alice.py -d
```

## cron起動

wheneverを入れてください

```
./setup.sh
```

```
vi ./config/schedule.rb
```

もしくはコピーして編集する

```
mkdir private
cp /config/schedule.rb private/schedule_hogehoge.rb
```

cronに登録
```
whenever -f private/schedule_hogehoge.rb
```

上記で出力された設定をcrontabにコピーする

crontabを全上書きしたい場合は以下

```
whenever -w -f private/schedule.rb 
```

## メモ

### CentOS Python3インストール方法

http://blog.umentu.work/?p=153