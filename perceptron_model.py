import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

N = 5  #記憶する手数
# x:入力層の時系列表現, w:重み, b:バイアス(切片), v:出力層
x = [[0 for _ in range(3)] for _ in range(N)]
w = [[[0 for _ in range(3)] for _ in range(N)] for _ in range(3)]
'''
x = [[0, 0, 0], [0, 0, 0], ... [0, 0, 0], -1]
w = [
     [[0, 0, 0], [0, 0, 0], ..., [0, 0, 0]],
     [[0, 0, 0], [0, 0, 0], ..., [0, 0, 0]],
     [[0, 0, 0], [0, 0, 0], ..., [0, 0, 0]],
    ]
'''
b = [0]*3
v = [0]*3

def predict(x, w, b):

    # vへの入力信号の算定
    v = [0]*3  # 初期化
    for k in range(3):
        for t in range(N):
            for c in range(3):
                v[k] += w[k][t][c] * x[t][c]
        v[k] += b[k] #バイアス項
    
    # 最大入力を受けたユニットを返す
    maxk = 0
    maxv = v[0]
    for k in range(1,3):
        if v[k] > maxv:
            maxv = v[k]
            maxk = k
    return maxk, v

def updateStates(player, x, w, v, b):
    # プレイヤーの手をバイナリー表現に変換
    prec = [-1, -1, -1]
    prec[player] = 1

    # 誤り訂正
    for k in range(3):
        if prec[k] * v[k] <= 0: #実際の手(prec[k])と予測した手v[k]が異符号だったら
            for t in range(N):
                for c in range(3):
                    w[k][t][c] += prec[k] * x[t][c]
            b[k] += prec[k] #バイアス項
    
    # 入力層xを3ビット分右にシフト
    for t in range(N-1, 0, -1):
        x[t] = x[t-1].copy()

    # プレイヤーの手(prec[0:2])を入力スロット最前列(x[0][0:2])に挿入
    x[0] = prec.copy()

    return x, w, b

#---じゃんけんのメインループ---
win = 0
lose = 0
draw = 0
total = 0

print("グー = 0, チョキ = 1, パー = 2")
while True:
    pred, v = predict(x, w, b)
    com = (pred+2)%3

    while True:
        try:
            player = int(input("何を出す？： "));
        except:
            print("0~2の数字を入力してください！")
            continue
        if player == -1:
            sys.exit()
        elif player < 0 or player > 2:
            print("0~2の数字を入力してください！")
        else:
            break

    print("AIの手： ", com)
    if player == com:
        print("あいこ！")
        draw += 1
    elif (com - player) % 3 == 1:
        print("勝ち！")
        win += 1
    else:
        print("負け！")
        lose += 1
    total += 1

    x, w , b = updateStates(player, x, w, v, b)

    print(f"勝率： 勝ち {win}  負け {lose}  あいこ {draw} / 計{total}回")