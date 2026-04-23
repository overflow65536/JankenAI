# JankenAI
プレイヤーの次の手を予測するじゃんけんAIを作ってみました．

## デモ
<img width="799" height="628" alt="Image" src="https://github.com/user-attachments/assets/f9f462e3-69e8-46a9-86a0-7ff09e831b1c" />

## ファイルの説明
* markov_model.py - マルコフ連鎖を応用したじゃんけんの予測モデル
* markov_jankenGUI - ↑のtkinter実装版．プレイ画面と勝率推移を表示
* perceptron_model.py - 単純パーセプトロンを応用したじゃんけんの予測モデル
* perceptron_jankenGUI - ↑のtkinter実装版．

## 参考
[AIじゃんけんマシン (篠本滋先生)](https://s-shinomoto.com/janken/japanese.html) と[C試作プログラム](https://s-shinomoto.com/janken/c.html)

perceptron_model.pyの中身の計算は引用元のコードを参考に作っています．
