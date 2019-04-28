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

分類結果の抜粋
```
欅って、書けない？                                   [170508-0035][GR23][テレビ東京１]欅って、書けない？.mp4
僧侶と交わる色欲の夜                                [170508-0100][GR16][ＴＯＫＹＯ　ＭＸ１]僧侶と交わる色欲の夜に….mp4
浅草ベビ                                          [170508-0105][GR23][テレビ東京１]浅草ベビ９.mp4
銀魂                                             [170508-0135][GR23][テレビ東京１]銀魂「少年はカブト虫を通し生命の尊さを知る」.mp4
あおほし                                          [170508-0230][GR18][ｔｖｋ１]あおほし.mp4
世界の闇図                                         [170508-0405][GR23][テレビ東京１]世界の闇図鑑　第６闇.mp4
ドロンコロン                                         [170508-0455][GR18][ｔｖｋ１]ドロンコロン.mp4
フランダース                                        [170508-0600][GR16][ＴＯＫＹＯ　ＭＸ２]フランダースの犬.mp4
ウルトラマンティガ                                    [170508-0700][GR18][ｔｖｋ１]ウルトラマンティガ.mp4
連続テレビ小説                                      [170508-0800][GR27][ＮＨＫ総合１・東京]連続テレビ小説　ひよっこ.mp4
相棒                                              [170508-1555][GR24][テレビ朝日]相棒１５.mp4
ベイブレードバースト                                   [170508-1755][GR23][テレビ東京１]ベイブレードバースト　ゴッド.mp4
雷様剣士ダイジ                                      [170508-1815][GR18][ｔｖｋ１]雷様剣士ダイジ.mp4
```
