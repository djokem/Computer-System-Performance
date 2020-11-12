import numpy as np
import scipy.linalg as splin

def buzen_optimized(x_vect, n):

    G = [0] * (n + 1)
    G[0] = 1
    x_list = x_vect.T[0]
    for xi in (x_list):
        for j in range(1, n + 1):
            G[j] = G[j] + G[j - 1] * xi

    return G



def s_kor_disks(k):

    s = [5, 20, 15, 15]
    sk = [20]*k
    s = s + sk

    return s

def rezultati_analiticki(X, N, x, K):

    G = buzen_optimized(X, N)
    usages = [xi * G[N-1] / G[N] for xi in x]
    productivities = [usagei * ui for usagei, ui in zip(usages, u)]  # Xi = Ui / si = Ui * ui

    X_sis = 0.1 * productivities[0]
    T = N / X_sis

    J = [0]
    J.clear()
    for xi in x:
        ji= sum([pow(xi,i)*G[N-i]/G[N] for i in range(1,N+1)])
        J.append(ji)

    file2.write("Broj korisnickih diskova K = " + str(K) +"\n")
    file2.write("Stepen multiprogramiranja N = " + str(N) + "\n\n")
    file2.write("Vreme odziva sistema T = " + str('{0:.3g}'.format(T)) + "\n")
    file2.write("Iskoriscenja resursa:\n")
    j = 1
    for i in usages:
        file2.write("U" + str(j) + " = " + str('{0:.3g}'.format(i)) + "; ")
        j = j + 1
    else:
        file2.write("\n")

    file2.write("Protoci kroz resurse:\n")
    j = 1
    for i in productivities:
        file2.write("X" + str(j) + " = " + str('{0:.3g}'.format(i)) + "; ")
        j = j + 1
    else:
        file2.write("\n")

    file2.write("Prosecan broj poslova kroz resurse:\n")
    j = 1
    for i in J:
        file2.write("J" + str(j) + " = " + str('{0:.3g}'.format(i)) + "; ")
        j = j + 1
    else:
        file2.write(
            "\n-----------------------------------------------------------------------------------------------------------------------\n\n")

file1 = open('potraznje_analiticki.txt', 'w')
file2 = open('rezultati_analiticki.txt', 'w')
for x in range(2,9):
    s = s_kor_disks(x)
    u = [1000/si for si in s]
    dim = len(s)

    P1 = [0.1, 0.1, 0.1, 0.1] + [0.6/x]*x
    P2 = [1, 0, 0, 0] + [0]*x
    P3 = [1, 0, 0, 0] + [0]*x
    P4 = [1, 0, 0, 0] + [0]*x

    P = [P1,P2,P3,P4]
    for y in range(x):
        pi = [1] + [0] * 3 + [0] * x
        P.append(pi)

    P = np.mat(P)
    # file1.write("\n\nGordon-Njuelova matrica tranzicije P :\n")
    # np.savetxt(file1,P,delimiter=", ",fmt='%1.3f')
    # file1.write("\n\n")
    # print("Za K = ",x,"\nP:\n",P,"\n")

    A = np.mat(P).T - np.identity(dim)
    # file1.writelines("A = P.T - I : \n")
    # np.savetxt(file1,A,delimiter=", ",fmt='%1.3f')
    # print("A = P.T - I : ", "\n", A)

    U = [[0]*i + [ui] + [0]*(dim-i-1) for i, ui in enumerate(u)]
    U = np.mat(U)
    # file1.write("U :\n")
    # np.savetxt(file1,U,delimiter=", ",fmt='%1.3f')
    # file1.write("\n\n")
    # print("U : ","\n",U, "\n")

    K = A * U
    # file1.write("K = A * U :\n")
    # np.savetxt(file1,K,delimiter=", ",fmt='%1.3f')
    # file1.write("\n\n")
    # print("K :\n", K, "\n")

    X = splin.null_space(K)
    X = X/X[0]
    xs = X.T[0]

    file1.write("Broj korisnickih diskova = ")
    file1.write(str(x) + "\n")
    file1.write("Potraznje :\n")
    j = 1
    for h in xs:
        file1.write("X" + str(j) + " = " + str('{0:.3g}'.format(h)) + "; ")
        j = j + 1
    else:
        file1.write("\n-----------------------------------------------------------------------------------------------------------------------\n\n")
    file1.write("\n")

    rezultati_analiticki(X, 10, xs, x)
    rezultati_analiticki(X, 15, xs, x)
    rezultati_analiticki(X, 20, xs, x)


file1.close()
file2.close()

