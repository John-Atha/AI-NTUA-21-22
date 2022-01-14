from copy import copy
import numpy as np
import pandas as pd
from tabulate import tabulate
import collections

rows = [
    [1, 0, -1, 4],
    [1, 4, 0, -1],
    [1, 2, 2, -1],
    [1, 3, -1, 0],
    [1, -2, 1, -3],
    [1, 0, -2, -1]
]

def make_xs(rows):
    def add_example(l, xs):
        l = np.array(l)
        xs.append(l)
    xs = []
    for row in rows:
        add_example(row, xs)
    return xs

xs = make_xs(rows)
ys = np.array(['B', 'A', 'B', 'A', 'B', 'A'])
w = np.array([1, 1, -1, -1])

def f(x):
    return int(x>=0)

vectorized_rounder = np.vectorize(lambda x: round(x, 2))

def train(xs, ys, f, w, learning_rate):
    arr = []
    head = ["Epoch", "(w0, w1, w2, w3)", "(x0, x1, x2, x3)", "Σwixi", "uk", "f(uk)", "yk-f(uk)", "b*(yk-f(uk))*xk", "w(k+1)"]
    
    prev_weight = copy(w)
    # weights_changed = [True for _ in range(len(xs))]
    same_weights_continuous = 0

    def is_train_over(epoch):
        nonlocal same_weights_continuous
        print("epoch:", epoch+1, " -> ", same_weights_continuous+1, " continuous weights remain the same")
        return same_weights_continuous==len(xs)-1
        
        # print("epoch:", epoch+1 , weights_changed)
        # return all(list(map(lambda x: not x, weights_changed)))

    epoch = 0
    while True:
        for k in range(len(xs)):
            arr_row = []
            arr_row.append(epoch+1)
            arr_row.append(w)
            x = xs[k]
            arr_row.append(x)
            sum_ = round(np.multiply(w, x).sum(), 2)
            arr_row.append(sum_)
            f_ = f(sum_)
            arr_row.append(f_)
            y = int(ys[k]=='B')
            arr_row.append(y)
            diff = y-f_
            arr_row.append(diff)
            dw = learning_rate * diff * x
            arr_row.append(dw)
            w = vectorized_rounder(w + dw)
            arr_row.append(w)
            arr.append(arr_row)
            if np.array_equal(w, prev_weight):
                # weights_changed[k] = False
                same_weights_continuous += 1
            else:
                # weights_changed[k] = True
                same_weights_continuous = 0
            prev_weight = copy(w)
            if is_train_over(epoch):
                print("STOPPING...")
                return arr, head, w
        epoch += 1

def classify(w, f, x):
    print(w, x)
    sum_ = round(np.multiply(w, x).sum(), 2)
    print(sum_)
    f_ = f(sum_)
    return 'B' if f_ else 'A'
    

arr, headers, w = train(xs, ys, f, w, 0.2)
print(tabulate(arr, headers=headers))
print('---'*10)
print('---'*10)
print('---'*10)
df = pd.DataFrame(arr, columns=headers)
df.to_csv('output.csv')


x = np.array([1, -1, 2, 2])
class_ = classify(w, f, x)
print(f"{x} belongs to class {class_}")