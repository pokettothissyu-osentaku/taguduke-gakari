# taguduke-gakari

ファイルをタグ管理するためのコマンドラインツールです


## インストール

```
$ pip install git+https://github.com/pokettothissyu-osentaku/taguduke-gakari.git
```


## 使い方

```
$ tagudu --help
INFO: Showing help with the command 'tagudu -- --help'.

NAME
    tagudu

SYNOPSIS
    tagudu COMMAND

COMMANDS
    COMMAND is one of the following:

     set
       ファイルに対してタグを設定

     remove
       ファイルからタグを解除

     remove_all
       ファイルからすべてのタグを解除

     autoremove
       タグが付けられているが実在しないファイルを削除

     tags
       ファイルに設定されているタグのリストを表示

     list
       タグがつけられているファイルのリストを表示

     existing_list
       タグ付け可能な実在するファイルのリストを表示

     nonexisting_list
       タグが付けられているが実在しないファイルのリストを表示

     unregistered_list
       タグがつけられていないファイルのリストを表示

     counts
       タグ数の集計を表示

     filter
       ファイルを絞り込む。指定されたタグのいずれかを含むファイルを対象とする（ORモード）

     filter_and
       ファイルを絞り込む。指定されたタグをすべて含むファイルを対象とする（ANDモード）

     filter_re
       正規表現によりファイルを絞り込む

     filter_partial
       ファイルを絞り込む。指定されたタグのいずれかが部分一致するファイルを対象とする

     reset
       ファイルの配置をリセットする
```


## ライブラリ

ライブラリとしても使えます

```python
from tagudu import TaggedDirectory

tagged_directory = TaggedDirectory("./")
tagged_directory.do_something()
```

[詳細](https://pokettothissyu-osentaku.github.io/taguduke-gakari/)
