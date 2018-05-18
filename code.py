#!/usr/bin/env python3

from __future__ import print_function

import sys
import numpy as np
import matplotlib.pyplot as plt
import itertools as it


# Generate D and visualise

def generate_D():
    product = list(it.product([-1, 1], repeat=9))
    D = []
    for d in product:
        D.append(np.reshape(np.asarray(d), (3, 3)))
    return D


def draw_D(data, m):
    print("Maximal dataset for H{}".format(m))
    for i in range(3):
        for j in range(3):
            if data[i][j] == -1:
                print("o", end=" ")
            else:
                print("x", end=" ")
        print()
    print()


# Represent each model
# def H0 -- inline in marginalise function

def M1(data, params):
    p = 1.0
    for i in range(3):
        for j in range(3):
            e = np.exp(-data[i, j]*params[0]*(i-1))
            p = p * 1/(1+e)
    return p


def M2(data, params):
    p = 1.
    for i in range(3):
        for j in range(3):
            e = np.exp(-data[i, j]*(params[0]*(i-1) + params[1]*(j-1)))
            p = p * 1/(1+e)
    return p


def M3(data, params):
    p = 1.
    for i in range(3):
        for j in range(3):
            e = np.exp(-data[i, j]*(params[0]*(i-1)+params[1]*(j-1)+params[2]))
            p = p * 1/(1+e)
    return p


# Sample from the prior

samples = 100

cov1 = (10**3)*np.eye(1)
mean1 = np.zeros(1)
params1 = np.random.multivariate_normal(mean1, cov1, samples)

cov2 = (10**3)*np.eye(2)
mean2 = np.zeros(2)
params2 = np.random.multivariate_normal(mean2, cov2, samples)

cov3 = (10**3)*np.eye(3)
mean3 = np.zeros(3)
params3 = np.random.multivariate_normal(mean3, cov3, samples)


# Monte Carlo integration

def marginalise(data, model, params):
    p = 0.0
    for i in range(samples):
        if model == 0:
            p = p + (1.0/512)
        if model == 1:
            p = p + M1(data, params[i])
        if model == 2:
            p = p + M2(data, params[i])
        if model == 3:
            p = p + M3(data, params[i])
    return p/samples


# Order data sets

def order_data_sets(data):
    # Create distance matrix
    size = data.shape[0]
    distance = np.zeros([size, size])
    for i in range(size):
        for j in range(size):
            distance[i, j] = data[i]-data[j]
            if i == j:
                distance[i, j] = np.inf

    L = []
    D = list(range(data.shape[0]))

    # Chose start of data set L as argmin
    LL = data.argmin()

    D.remove(LL)
    L.append(LL)

    while len(D) != 0:
        N = []

        # Find set of points in D with L as nearest neighbour
        for k in range(len(D)):
            # Get the nearest neighbour to D[k]
            n = distance[D[k], D].argmin()
            if D[n] == LL:
                N.append(D[n])
        if not N:
            # Choose nearest neighbour in D to L
            LL = D[distance[LL, D].argmin()]
        else:
            # Choose furthest point from L in N
            LL = N[distance[LL, N].argmin()]
        D.remove(LL)
        L.append(LL)
    return L


if (len(sys.argv) < 2):
    print("Please supply either graph or draw as an argument")
    exit(1)

data = np.zeros([4, 512])
d = generate_D()

for j in range(512):
    data[0][j] = marginalise(d[j], 0, None)
    data[1][j] = marginalise(d[j], 1, params1)
    data[2][j] = marginalise(d[j], 2, params2)
    data[3][j] = marginalise(d[j], 3, params3)

index = order_data_sets(np.sum(data, axis=0))


def graph(data):
    plt.figure(1)
    plt.plot(data[3, index], 'g', label="P($\mathcal{D}|{H}_3$)")
    plt.plot(data[2, index], 'r', label="P($\mathcal{D}|{H}_2$)")
    plt.plot(data[1, index], 'b', label="P($\mathcal{D}|{H}_1$)")
    plt.plot(data[0, index], 'm--', label="P($\mathcal{D}|{H}_0$)")
    plt.xlabel("All data sets, $\mathcal{D}$")
    plt.ylabel("Evidence")
    plt.legend()

    plt.figure(2)
    plt.plot(data[3, index], 'g', label="P($\mathcal{D}|{H}_3$)")
    plt.plot(data[2, index], 'r', label="P($\mathcal{D}|{H}_2$)")
    plt.plot(data[1, index], 'b', label="P($\mathcal{D}|{H}_1$)")
    plt.plot(data[0, index], 'm--', label="P($\mathcal{D}|{H}_0$)")
    plt.xlim(0, 80)
    plt.xlabel("Subset of possible data sets, $\mathcal{D}$")
    plt.ylabel("Evidence")
    plt.legend()

    plt.show()


if (sys.argv[1] == "graph"):
    graph(data)
elif (sys.argv[1] == "draw"):
    [draw_D(d[dat.tolist().index(max(dat))], m) for m, dat in enumerate(data)]
