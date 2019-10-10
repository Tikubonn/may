
# May 

![Python 3.6](https://img.shields.io/badge/Python-3.6-blue.svg "Python 3.6")
![MIT](https://img.shields.io/badge/License-MIT-green.svg "MIT")

\| 日本語 \| [English](README.md) \| 

May は FTP の通信をファイルシステムのように抽象化してくれるラッパーです。
このライブラリを使うことで FTP プロトコルを意識することなく接続先コンピュータのファイルを操作することができます。
ただし、実行速度よりも使いやすさを重視しているため、他のライブラリに比べてパフォーマンスは劣るかもしれません。

## Usage

まずは `open_may` 関数を `may` パッケージからインポートしましょう。
この関数はサーバとの接続を開始し、FTP を用いたサーバとのやり取りを抽象化してくれるインスタンスを作成します。
下記の例ではサーバとの接続を開始後にディレクトリを移動し、移動先のディレクトリにあるファイルをすべてダウンロードします。

```python3 
from may import open_may

may = open_may("localhost", user="tikubonn", passwd="passwd")
may.chdir("example")

for file in may.iterdir():
    if may.isfile(file):
        may.download(file, file.name) # download remote file to local.

may.close() # quit and close.
```

`open_may` 関数で作成されるインスタンスは with 文に対応しているため、以下のように書くこともできます。
例外の有無に関係なく処理が with ブロックを抜けた際にインスタンスは自動的に閉じられます。

```python3 
with open_may("localhost", user="tikubonn", passwd="passwd") as may:
    pass
```

もし SFTP を利用したい場合には代わりに `open_may_tls` 関数を利用することができます。

```python3
from may import open_may_tls
```

## Installation

May は [setup.py](setup.py) が同梱されているため下記のコマンドからインストールすることができます。

```shell
$ python setup.py install
```

## License 

May は [MIT License](LICENSE) の許諾の下で公開されています。
