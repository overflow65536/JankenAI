import random
import sys
import tkinter as tk
import random

#累計分布 (not正則分布)
distribution = [[0, 0, 0], 
                [0, 0, 0], 
                [0, 0, 0]]

'''
distribution = [[P(r|r), P(s|r), P(p|r)],
                [P(r|s), P(s|s), P(p|s)],
                [P(r|p), P(s|p), P(p|p)]]
'''

def predict(prev, d):
    # prev = 0 or 1 or 2
    s = sum(d[prev])
    r = random.uniform(0, s)
    if r < distribution[prev][0]:
        # プレイヤーが出しやすい手 = グー(0)
        pred = 0
    elif r < distribution[prev][0] + distribution[prev][1]:
        # プレイヤーが出しやすい手 = チョキ(1)
        pred = 1
    else:  # r < distribution[prev][0] + distribution[prev][1] + distribution[prev][2]
        # プレイヤーが出しやすい手 = パー(2)
        pred = 2
    
    return pred

#---じゃんけんのメインループ---
win = 0
lose = 0
draw = 0
total = 0

print("グー = 0, チョキ = 1, パー = 2")
prev = random.randint(0, 2)

while True:
    pred = predict(prev, distribution)  #プレイヤーの手を予測
    com = (pred+2)%3  #predに対して勝つ手

    #プレイヤー入力
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

    #勝敗判定
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

    #分布を更新
    if total != 0:
        distribution[prev][player] += 1
        prev = player

    print(f"勝率： 勝ち {win}  負け {lose}  あいこ {draw} / 計{total}回")