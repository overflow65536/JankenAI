import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

N = 5

class Parceptron:
    def __init__(self):
        self.x = [[0 for _ in range(3)] for _ in range(N)]
        self.w = [[[0 for _ in range(3)] for _ in range(N)] for _ in range(3)]
        self.b = [0]*3

    def predict(self):
        v = [0]*3
        for k in range(3):
            for t in range(N):
                for c in range(3):
                    v[k] += self.w[k][t][c] * self.x[t][c]
            v[k] += self.b[k]

        maxk = 0
        maxv = v[0]
        for k in range(1,3):
            if v[k] > maxv:
                maxv = v[k]
                maxk = k

        return maxk, v

    def update(self, player, v):
        prec = [-1, -1, -1]
        prec[player] = 1

        for k in range(3):
            if prec[k] * v[k] <= 0:
                for t in range(N):
                    for c in range(3):
                        self.w[k][t][c] += prec[k] * self.x[t][c]
                self.b[k] += prec[k]

        for t in range(N-1, 0, -1):
            self.x[t] = self.x[t-1].copy()

        self.x[0] = prec.copy()


class App:
    def __init__(self, root):
        self.ai = Parceptron()

        rock = Image.open("rock.png")
        scissors = Image.open("scissors.png")
        paper = Image.open("paper.png")
        rock = rock.resize((60, 60))
        scissors = scissors.resize((60, 60))
        paper = paper.resize((60, 60))
        self.rock = ImageTk.PhotoImage(rock)
        self.scissors = ImageTk.PhotoImage(scissors)
        self.paper = ImageTk.PhotoImage(paper)

        self.win = 0
        self.lose = 0
        self.draw = 0
        self.total = 0

        self.history_winrate = []
        self.history_loserate = []
        self.history_drawrate = []

        root.title("じゃんけんAI パーセプトロン版")
        root.geometry("800x600")
        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)

        # --- プレイ画面UI ---
        top = tk.Frame(root)
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure((0,1,2), weight=1)

        self.label = tk.Label(top, text="じゃんけん！")
        self.label.grid(row=0, column=0, columnspan=3, pady=5)

        self.ai_hand_label = tk.Label(top, relief=tk.SOLID, bd=3)
        self.ai_hand_label.grid(row=1, column=0, columnspan=3, pady=10)

        tk.Button(top, image=self.rock, command=lambda: self.play(0)).grid(row=2, column=0, sticky="ew")
        tk.Button(top, image=self.scissors, command=lambda: self.play(1)).grid(row=2, column=1, sticky="ew")
        tk.Button(top, image=self.paper, command=lambda: self.play(2)).grid(row=2, column=2, sticky="ew")

        self.result_label = tk.Label(top, text="")
        self.result_label.grid(row=3, column=0, columnspan=3)

        # --- 戦績グラフ ---
        bottom = tk.Frame(root)
        bottom.grid(row=1, column=0, sticky="nsew")
        bottom.rowconfigure(0, weight=1)
        bottom.columnconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=bottom)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def play(self, player):
        pred, v = self.ai.predict()
        com = (pred + 2) % 3

        if player == com:
            result = "あいこ"
            self.draw += 1
        elif (com - player) % 3 == 1:
            result = "勝ち"
            self.win += 1
        else:
            result = "負け"
            self.lose += 1

        img_map = [self.rock, self.scissors, self.paper]
        self.ai_hand_label.config(image=img_map[com])

        # 学習
        self.ai.update(player, v)

        # 勝率更新
        self.total = self.win + self.lose + self.draw
        self.history_winrate.append(self.win)
        self.history_loserate.append(self.lose)
        self.history_drawrate.append(self.draw)

        self.update_graph()

    def update_graph(self):
        self.ax.clear()
        self.ax.plot(self.history_winrate, label="You Win", color="red")
        self.ax.plot(self.history_loserate, label="AI Win", color="blue")
        self.ax.plot(self.history_drawrate, label="Draw", color="yellow")
        self.ax.set_title("Record")
        self.ax.legend(loc=1)
        self.ax.set_ylim(0, self.total)
        self.canvas.draw()

root = tk.Tk()
app = App(root)
root.mainloop()