const N = 5;

// 状態
let x = Array.from({length: N}, () => [0,0,0]);
let w = Array.from({length: 3}, () =>
    Array.from({length: N}, () => [0,0,0])
);
let b = [0,0,0];

let win = 0, lose = 0, draw = 0;

// --- 予測 ---
function predict() {
    let v = [0,0,0];

    for (let k = 0; k < 3; k++) {
        for (let t = 0; t < N; t++) {
            for (let c = 0; c < 3; c++) {
                v[k] += w[k][t][c] * x[t][c];
            }
        }
        v[k] += b[k];
    }

    let maxk = 0;
    let maxv = v[0];
    for (let k = 1; k < 3; k++) {
        if (v[k] > maxv) {
            maxv = v[k];
            maxk = k;
        }
    }

    return [maxk, v];
}

// --- 学習 ---
function update(player, v) {
    let prec = [-1, -1, -1];
    prec[player] = 1;

    for (let k = 0; k < 3; k++) {
        if (prec[k] * v[k] <= 0) {
            for (let t = 0; t < N; t++) {
                for (let c = 0; c < 3; c++) {
                    w[k][t][c] += prec[k] * x[t][c];
                }
            }
            b[k] += prec[k];
        }
    }

    // シフト
    for (let t = N-1; t > 0; t--) {
        x[t] = [...x[t-1]];
    }

    x[0] = [...prec];
}

// --- ゲーム ---
function play(player) {
    let [pred, v] = predict();
    let com = (pred + 2) % 3;

    let result = "";

    if (player === com) {
        result = "あいこ";
        draw++;
    } else if ((com - player + 3) % 3 === 1) {
        result = "勝ち";
        win++;
    } else {
        result = "負け";
        lose++;
    }

    document.getElementById("result").innerText =
        `AI: ${["グー","チョキ","パー"][com]} → ${result}`;

    document.getElementById("score").innerText =
        `勝ち:${win} 負け:${lose} あいこ:${draw}`;

    // 学習
    update(player, v);
}