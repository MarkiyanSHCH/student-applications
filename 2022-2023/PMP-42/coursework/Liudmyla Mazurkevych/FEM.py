# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sElLxIsImszdg9cJqSFphVTdeMz37_ql
"""

import numpy as np
from scipy.sparse import lil_matrix
from scipy.special import legendre
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
eps = np.finfo(float).eps

V = 1.0
D = 100.0
R = 1.0
f = 1.0

a = 0.0
b = 1.0

N = 64
M = N + 1

x = np.linspace(a, b, M)



K = lil_matrix((M, M))
A = lil_matrix((M, M))
B = lil_matrix((M, M))
F = np.zeros(M)

for e in range(N):
    x_e = x[e:e+2]

    Ke = np.zeros((2, 2))
    Ae = np.zeros((2, 2))
    Re = np.zeros((2, 2))
    Fe = np.zeros(2)

    h = x_e[1] - x_e[0]
    Ke[0, 0] = D / h
    Ke[0, 1] = -D / h
    Ke[1, 0] = -D / h
    Ke[1, 1] = D / h

    Ae[0, 0] = V / 2
    Ae[0, 1] = V / 2
    Ae[1, 0] = -V / 2
    Ae[1, 1] = -V / 2

    Re[0, 0] = h * R / 3
    Re[0, 1] = -h * R / 6
    Re[1, 0] = -h * R / 6
    Re[1, 1] = h * R / 3

    Fe[0] = f * h / 2
    Fe[1] = f * h / 2

    indices = [e, e+1]
    K[np.ix_(indices, indices)] += Ke
    A[np.ix_(indices, indices)] += Ae
    B[np.ix_(indices, indices)] += Re
    F[indices] += Fe
    if (x_e[0] - a) < eps:
      K[e, e] = 1e15
    if (b - x_e[1]) < eps:
      K[e, e] = 1e15

c_a = 1.0
c_b = 1.0

alpha_a = 1.0
alpha_b = 1.0


K[0, 0] += alpha_a
K[0, 1] -= alpha_a


K[M-1, M-1] += alpha_b
K[M-1, M-2] -= alpha_b


C = spsolve((K + A + B).tocsr(), F)

# Точний розв'язок
alpha_1 = (-V + np.sqrt(V**2 + 4 * D * R)) / (-2 * D)
alpha_2 = (-V - np.sqrt(V**2 + 4 * D * R)) / (-2 * D)
c_exact = (f / R) * (((np.exp(alpha_2 * b) - 1) / (np.exp(alpha_1 * b) -
np.exp(alpha_2 * b))) * np.exp(alpha_1 * x) + ((1 - np.exp(alpha_1 * b)) /
 (np.exp(alpha_1 * b) - np.exp(alpha_2 * b))) * np.exp(alpha_2 * x) + 1)



plt.plot(x, C, label='Numerical Solution')
plt.plot(x, c_exact, label='Exact Solution')
plt.xlabel('x')
plt.ylabel('Concentration')
plt.title('Concentration Profile')
plt.legend()
plt.grid(True)
plt.show()



print("Numerical Solution:")


print("Exact Solution:")
print(c_exact)

relative_error = np.linalg.norm(c_exact - C) / np.linalg.norm(c_exact)*100
print("Relative Error:", relative_error)