
## 構造
- `main.py` : 文字通りメインの部分です。他の `/service` にあるpythonファイルたちに支えられています。
- `/input_file` : 入力ファイルです。
- `/output_file` : コードを整理する前に出力されたファイルたちです。整理したときにおかしなことになってないかテストに使いました。確認用にどうぞって感じです。
- `/new_output_file` : コードを整理した後に出力されたファイルたちです。こっちが本体。
- `test.py` : output_fileの中身とnew_output_fileの中身を比較して出力が変わってないか確認します。
- `/service` : 動作をサポートするpythonファイルが入っています
  - `data_frame_handler.py` : pandasのdataframeの機能を拡張したような使い方をしています。
  - `file_handler.py` : ファイルのパスを提供します。入出力のファイルを変更した際はこちらも修正が必要です。

## 実行環境
```bash
$ python --version
  >> Python 3.9.6
```

## 実行方法
```bash
$ python main.py
  ~~~~~ 
```
これだけ