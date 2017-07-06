主に録画したファイルを自動で分別するためのスクリプトです。
元のディレクトリからターゲット/{カテゴリー名} にmvさせます。

# SetUp   
```angular2html
pip3 install requests
```
  
# How to use it  
```
wget https://raw.githubusercontent.com/stdll00/RecCategorize/master/rec_categorize.py
./rec_categorized.py recorded_file_dir categorized_dir
```
確認画面で y でファイルをmvさせる  

categorized_dirに予めカテゴリの名前のディレクトリを作成しておくと類似しているファイルが自動的に分別されます。


# アルゴリズム  
target_dirに含まれるもの及び
http://qiita.com/AKB428/items/64938febfd4dcf6ea698
にあるapi.moemoe.tokyo/anime/v1/master/:year 
のデータ、
ファイル名から分類しています。


# GoogleDrive (GooglePhotos) での利用  
GoogleDriveを同期させて利用してください。　　
ディスク容量等で同期が不可能な場合は
GoogleDrive Ocamlfuseでマウントして使ってください(動作確認ずみ)
https://github.com/astrada/google-drive-ocamlfuse
