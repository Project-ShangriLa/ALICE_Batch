from bs4 import BeautifulSoup
import sys
import re
from pprint import pprint

# python3 sample_view_total_count.py html_cache/lovelive20161110.html

argvs = sys.argv

## 設定ファイルを読み込み

## JSONをデコード

## 配列をループして処理

## キーワードごとにファイルダウンロード

## パース

search_word = ""

html = open(argvs[1])

bsObj = BeautifulSoup(html.read(), "html.parser")

#  <h2>このタグがついたpixivの作品閲覧データ <span class="total-count">総閲覧数: 37897330</span></h2>
total_count = bsObj.find("span", class_="total-count").string

#'総閲覧数: 37897330'


print(total_count.replace("総閲覧数: ", ""))

total_count_i = int(total_count.replace("総閲覧数: ", ""))


## 履歴を保存(通常はhourly)


