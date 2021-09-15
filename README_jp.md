# M5Stack 用 SDFont micropython モジュール

このリポジトリでは、M5Stack の UiFlow 環境でCJK(中国語、日本語、韓国語)フォントを活用する micropyhon モジュールを提供しています。

English README is [here](./README_jp.md)

# 1. はじめに

UiFlow は若者やライトコーダー向けに非常に素晴らしいプログラミング環境なのですが、残念ながら CJKフォントの整備が遅れていました。v1.8.x では unicode フォントが利用できますが、UI 上の ラベルでしか使えませんし、サイズも 24px に限られています。しかも、カタカナの”－”(伸ばす棒)や”・”（中点）が正しく表示されません。(この件はBug Report でも報告はしていますが、UiFlow v1.8.3 の時点では、まだ改善されてはいません)

WEB 上ではArduino Library 向けに、いくつかの日本語表示方法などが紹介されていますが、UiFlow 向けの 方法はほとんど見つけられませんでした。簡単な方法で UiFlow でも SDカードに置いたフォントが使えるようにならないかなど自分自身でも調べてみましたが、うまい方法は見つかりませんでした。

ないならば作れということで、SDFont module と UiFlow 向けのカスタムブロックを作ることにしました。


# 2. 主な機能
SDFont モジュールはCJKフォントを用いた文字列を表示する基本的な機能と、いくつかの拡張機能を提供します。主な機能は以下の通りです。

 1. SD-card 上のフォントを利用
 2. 横書き、縦書きの文字列表示
 3. ワイプ、タイプライターなどのエフェクト
 4. 矩形内での複数行文字列表示
 5. 矩形内での複数ページに渡る文字列表示
 6. 表示速度の調整
 7. 行間の遅延時間設定
 8. SDFont 用の UiFlow カスタムブロック
 
このモジュールは、SDカード上のpython ファイルとして作成された専用フォントデータを利用します。

# 3. CJKフォントの準備
まず始めに、SDFont モジュールで利用するフォントファイルを準備する必要があります。 ここでは、簡単な方法として、 [micropython-font-to-py](https://github.com/tatnish/micropython-font-to-py) という python スクリプトを利用してTrueType/OpenTypeフォントを変換する方法を紹介します。
このスクリプトは Pter Hinch 氏により開発されたもので、文字数の多い CJK フォントを変換するために私が変更を加えたものです。
 
## 3.1 フォント変換スクリプトのインストール方法

### Windows 10

 1. python3 (現時点では 3.9 が最新版) を Microsoft Store からインストールする
 2. [micropython-font-to-py](https://github.com/tatnish/micropython-font-to-py) をダウンロードする (仮に C:\App\font-to-py\ とします)
 3. コマンドプロンプト又は Windows PowerShell を起動する
 4. コマンドラインで、freetype python モジュールをインストールする
   `pip3 install freetype-py`
 5. mpy-cross という python のクロスコンパイラをインストールする
   `pip3 install mpy-cross`
 6. font-to-py.py ファイルを、このリポジトリのローカルコピーの tools フォルダにコピーする

### Linux (Ububtu)

ターミナルから、以下のコマンドで必要なものをインストールします
 `apt install python3`
 `pip3 install freetype-py`
 `pip3 install mpy-cross`
 `git clone https://github.com/tatnish/SDFont.git
 `cd SDFont-master/tools`
 `git clone https://github.com/tatnish/micropython-font-to-py.git`
 `cp micropython-font-to-py-master/*.py .`
 
## 3.2 フォントの変換方法 (横書き用)

 1. 変換対象となる文字列のファイルを生成する。[tools/jisx0208.py](./tools/jisx0208.py) を使い、以下のコマンドを実行ください
   `python3 jisx0208.py > chars.txt`
 2. 変換する TrueType/OpenType フォントファイルをダウンロードする
 3. [micropython-font-to-py](https://github.com/tatnish/micropython-font-to-py) を使い、フォントを変換する. 以下のコマンドでは somefont.ttf から chars.txt で指定された文字の24px フォントファイルを生成します。
   `python3 font_to_py.py -k chars.txt somefont.ttf 24 somefont24.py`
  4. フォントファイル (.py) をコンパイルする
    `mpy-cross -O3 somefont24.py -march=xtensawin -X emit=native -somefont24.py -X heapsize=8000000`
  
  これにより、somefont24.mpy というようなフォントファイルが生成されます。
   
  注記: コンパイル時に メモリアロケーションエラーが出た場合は、heapsize=xxxxxxxx の値を 8000000 や 12000000 などに増加してください。

## 3.3 フォントの変換方法 (縦書き用)

縦書き用のフォントデータを作成するには、[サブセットフォントメーカー (subset font maker)](https://opentype.jp/subsetfontmk.htm) というツールを使い、元のフォントファイルから、縦書き用のフォントデータを含むTrueType/OpenTypeフォントファイルを生成する必要があります。

1.  [サブセットフォントメーカー](https://opentype.jp/bin/subsetfont320.msi) をダウンロードする
2. **作成元フォントファイル** を指定する
3. **作成後のフォントファイル** を指定する
4. **変換する文字列** を"フォントに格納するファイル(C)" テキストボックスに記述する
	* 日本語の場合 [tools/jisx0208.py](./tools/jisx0208.py) で出力したファイルから全ての文字列をコピペしてください
5. **文字組方向(A)** から **縦書き(V)**  を選択する
6. ** 書体名を変更する(G)** の選択を外す 
7. **作成開始** ボタンをクリックする
8. 3.2 フォントの変換方法 (横書き用)の手順に沿って .mpy ファイルを生成する
 
# 4. SDFont モジュールとフォントのインストール方法

1. [sdfont.py](./tools/sdfont.py) を以下のコマンドでコンパイルする 
  `mpy-cross -O3 sdfont.py -march=xtensawin -X emit=native -X heapsize=8000000` 
2. sdfont.mpy と、変換した .mpy のフォントファイルをSD-card の /fonts/ フォルダ内にコピーする

注記: **fonts** フォルダは、SD-card のルートフォルダ直下に作成してください。sdfont モジュールでフォントを読み込むときには、SDカード内の /fonts フォルダを参照します。

# 5. UiFlow でのフォントの使い方 (デモ)

SDFont モジュールとカスタムブロックにより、簡単に[UiFlow](http://flow.m5stack.com) 上で日本語の文字列を表示することができます。まずはデモプログラムを動作させてみましょう。

  1. 以下のファイルを SDカードの /fonts/ フォルダにコピーし、M5Stack へ挿入する
          * [sdfont.mpy](./sdfont.mpy)
	  * フォントファイル
	    * [クリーOne](./examples/demo/KleeOne24jp.mpy)
	    * [Pixel-M-PLUS12R](./examples/demo/Pixel-M-PLUS12R-24jp.mpy)
	    * [ステッキB](./examples/demo/Stick40jp.mpy)
	  * [title.jpg](./examples/demo/title.jpg)
	  * [RPGMap.jpg](./examples/demo/RPGMap.jpg)
  2.[UiFlow]((http://flow.m5stack.com) をブラウザで開く
  3. M5Stack core2 の API Key を指定する
  4. 以下の カスタムブロックを UiFlow に追加する (ブロックの一番下にある Custom を開き、 Open *.m5b をクリックします)
	 * [Graphics.m5b](./uiflow/Graphics.m5b)
	 * [SDFont.m5b](./uiflow/SDFont.m5b)
  5. デモアプリ [SDFontDemo.m5f](./examples/demo/SDFontDemo.m5f) を UiFlow に読み込む (右上の三本線ボタンを押し、Open を選ぶ)
  6. メニューの "▶(Play)" ボタンを押し、実行する

デモアプリのプログラムを見ることで、大体どんな処理をしているかが理解できます. 6章のカスタムブロックの説明を併せて参照ください。

# 6. SDFont 用カスタムブロック

### loadFont

読み込むフォント名を指定します。フォント名は、SDカードの /fonts/ フォルダ内にある フォントファイルの .mpy を省略したものです。 
  (例: フォンとファイル名が somefont24.mpy の場合は、 "somefont24")

* パラメタ: **文字列**: フォント名

### print

画面上に文字列を横書きします。パラメタは以下の通りです。

* text: **string**: 描画する文字列
* x: **number**: X座標(又は CENTER ブロック)  
* y: **number**: Y座標 (又は CENTER ブロック)
* effect: **number**: 以下のブロックのいずれかを指定します
	* No Effect: エフェクトなし 
	* Wipe Effect: 文字を1ラインずつ描画
	* Typewriter Effect: タイプライターのように１文字ずつ順に描画

### vprint

画面上に文字列を縦書きします。パラメタは以下の通りです。

* text: **string**: 描画する文字列
* x: **string**: X座標(又は CENTER ブロック)  
* y: **string**: Y座標 (又は CENTER ブロック)
* effect: **number**: 以下のブロックのいずれかを指定します
	* No Effect: エフェクトなし 
	* Wipe Effect: 文字を1ラインずつ描画
	* Typewriter Effect: タイプライターのように１文字ずつ順に描画

注記: 縦書きをするには、縦書き用のフォントファイルを作成してください。横書き用フォントファイルを使うと、「、」や「。」「ー」などの文字が正しく表示されません。

### printInRect

矩形内に複数行に渡る文字列を表示します。文字列が長い場合は、自動的にページを更新するので、ニュースリーダーやブックリーダーとしても利用できます。

*text: **string**: 表示する文字列。長い文字列は自動的に改行、改ページされます。  
* x: **string**: 矩形左上のX座標
* y: **string**: 矩形左上のY座標
* width: **number**: 矩形の幅 (ピクセル)
* height: **number**: 矩形の高さ (ピクセル)
* color: **number**: テキストの色 (例 0xffffff が白)
	* Graphics カスタムブロックの 色ブロック (例: **WHITE color**) を指定すると便利です
* effect: **number**: 以下のブロックのいずれかを指定します
	* No Effect: エフェクトなし 
	* Wipe Effect: 文字を1ラインずつ描画
	* Typewriter Effect: タイプライターのように１文字ずつ順に描画

### vprintInRect

矩形内に縦書きで文字列を表示します。文字列が長い場合は、自動的にページを更新するので、ニュースリーダーやブックリーダーとしても利用できます。
パラメタは、printInRect と同じです。

注記: 縦書きをするには、縦書き用のフォントファイルを作成してください。横書き用フォントファイルを使うと、「、」や「。」「ー」などの文字が正しく表示されません。

### setWipeDelay

Wipe Effect の遅延時間をミリ秒単位で指定します。 1 か 2 で効果が分かりやすい速度になります。5を指定すると、とても遅くなります。この設定値は print, vprint, printInRect, and vprintInRect ブロックで Wipe Effect を指定した時に利用されます。

* パラメタ: **number** 遅延量 (ミリ秒)

### setLineDelay

printInRect と vprintInRect ブロックで次の行を表示するまでの遅延時間をミリ秒で指定します。

* パラメタ: ** number** 遅延量 (ミリ秒)

### setPageDelay

printInRect と vprintInRect ブロックで次の行を表示するまでの遅延時間をミリ秒で指定します。1000ms から1500ms 程度が読みやすいでしょう。

* パラメタ: ** number** 遅延量 (ミリ秒)

### 

### Wipe Effect, Typewritter Effect, 及び No Effect

これらのブロックは、 print, vprint, printInRect, 及び vprintInRect ブロックの effect パラメタとして利用され、それぞれ以下の意味を持ちます。

* **No Effect**: 表示効果なし. 行単位で文字列が表示されます 
* **Wipe Effect**: ワイプ効果 (各文字のフォントデータが1行ずつ順に表示されます)
* **Typewriter Effect**: タイプライター効果 (１文字ずつ順に表示します)

### CENTER

このブロックは、文字列を画面の中央に配置したいときに利用されます。X座標、Y座標のパラメタとして利用することで、文字列を水平、垂直方向の中心に配置するようにX座標あるいはY座標が自動計算されます。 **print**, **vprint**, **printInRect**, 及び **vprintInRect**  のX座標、またはＹ座標の値として利用できます。

### textWidth

与えられた文字列を **loadFont** で指定したフォントで描画した際の幅をピクセル単位で返します。

* Parameter: **string**: 文字列


# 制限事項

このモジュールは micropython で記述されているため、実行速度は遅いです。
文字列描画には数十ミリ秒を要し、フォント読み込みには、ファイルサイズにも寄りますが、数秒から十秒程度かかることがあります。

.mpy のフォントデータはフリーズされた際にメモリ利用量が削減される設計ですが、ファームウェアに組み込まれないとフリーズされないため 
フォントデータ分のメモリを消費します。
このため、複数のフォントを読み込んだり、サイズの大きいフォントを読み込むとメモリアロケーションエラーが発生します。
このエラーが発生すると、フォントを読み込まないため、エラー前に読み込んでいたフォントを使うか、あるいは "get_ch is not defined" などの
エラーが発生します。

