主に録画したファイルを自動で分別するためのスクリプトです。
元のディレクトリからターゲット/{カテゴリー名} にmvさせます。

#SetUp
```angular2html
pip3 install requests
```

#How to use it
```
./rec_categorized.py recorded_file_dir categorized_dir
```
確認画面で y で移動させる



#アルゴリズム
target_dirに含まれるもの及び
http://qiita.com/AKB428/items/64938febfd4dcf6ea698
にあるapi.moemoe.tokyo/anime/v1/master/:year 
のデータ、
ファイル名から分類しています。
