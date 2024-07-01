def HSV2RGB(H, S, V):
    C = V*S
    H2 = H/60.0
    X = C*(1 - abs(H2%2 - 1))
    if H2 >= 0 and H2 < 1:
        R = C
        G = X
        B = 0
    elif H2 >= 1 and H2 < 2:
        R = X
        G = C
        B = 0
    elif H2 >= 2 and H2 < 3:
        R = 0
        G = C
        B = X
    elif H2 >= 3 and H2 < 4:
        R = 0
        G = X
        B = C
    elif H2 >= 4 and H2 < 5:
        R = X
        G = 0
        B = C
    elif H2 >= 5 and H2 < 6:
        R = C
        G = 0
        B = X
    else:
        R = 0
        G = 0
        B = 0
    return (R, G, B)

