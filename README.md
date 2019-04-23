主に録画したファイルを自動で分別するためのスクリプトです。
元のディレクトリからターゲット/{カテゴリー名} にmv or シンボリックリンクさせます。

![emby]( https://github.com/stdll00/RecCategorize/blob/master/emby1.png?raw=true )

自動振り分けしたディレクトリで[emby](https://emby.media/)のTV Show機能でmetadata自動ダウンロード機能を使用した場合の画像。  
`-y -l`オプションをつけ定期実行しています。  
タイトル部分はこのスクリプトが作成しており、アニメのデータベースと紐付いてNetflixのようなUIになります。

# SetUp   
```angular2html
pip3 install requests
```
  
# How to use it  
```
wget https://raw.githubusercontent.com/stdll00/RecCategorize/master/rec_categorize.py

chmod +x rec_categorize.py
./rec_categorized.py recorded_file_dir categorized_dir
```
確認画面で y でファイルをmvさせる  

categorized_dirに予めカテゴリの名前のディレクトリを作成しておくと類似しているファイルが自動的に分別されます。


# アルゴリズム  
target_dirに含まれるもの及び
http://qiita.com/AKB428/items/64938febfd4dcf6ea698
にあるapi.moemoe.tokyo/anime/v1/master/:year 
のデータ、ファイル名から分類しています。


# オプション
```
-y : 確認画面をスキップ
-l : mvの代わりにシンボリックリンクを作成
```

# サンプル
サンプルデータの振り分け結果です。概ね正しく動いています。  
https://github.com/stdll00/RecCategorize/blob/master/testout.txt
