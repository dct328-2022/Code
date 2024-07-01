import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.lines as mlines


class readfile:
    def __init__(self, infile, outfile, difflimit):
        content = open(infile)
        newf = open(outfile, 'w')
        Uy1 = []
        Fy1 = []
        Uy2 = []
        Fy2 = []
        a1 = 0
        a2 = 0
        a3 = 0
        a4 = 0
        for line in content:
            words = line.split()
            if len(words) > 0:
                try:
                    temp = float(words[0])
                except:
                    temp = 'No'
                if type(temp) == float:
                    X1 = float(words[1])
                    F1 = float(words[0])
                    X2 = float(words[3])
                    F2 = float(words[2])
                    #print('X1', X1, 'F1', F1, 'a1', a1, 'X2', X2, 'F2', F2, 'a3', a3)
                    if abs(X1) < difflimit[0] and abs(F1) - abs(a1) > difflimit[1]:
                        Fy1.append(F1)
                        Uy1.append(X1)
                        a1 = F1
                        a2 = X1

                    elif abs(X1) >= difflimit[0] and abs(X1) < difflimit[2] and abs(F1) - abs(a1) > difflimit[3]:
                        Fy1.append(F1)
                        Uy1.append(X1)
                        a1 = F1
                        a2 = X1

                    elif abs(X1) >= difflimit[2] and abs(X1) < difflimit[4] and abs(F1) - abs(a1) > difflimit[5]:
                        Fy1.append(F1)
                        Uy1.append(X1)
                        a1 = F1
                        a2 = X1

                    if abs(X2) < difflimit[0] and abs(F2) - abs(a3) > difflimit[1]:
                        Fy2.append(F2)
                        Uy2.append(X2)
                        a3 = F2
                        a4 = X2

                    elif abs(X2) >= difflimit[0] and abs(X2) < difflimit[2] and abs(F2) - abs(a3) > difflimit[3]:
                        Fy2.append(F2)
                        Uy2.append(X2)
                        a3 = F2
                        a4 = X2

                    elif abs(X2) >= difflimit[2] and abs(X2) < difflimit[4] and abs(F2) - abs(a3) > difflimit[5]:
                        Fy2.append(F2)
                        Uy2.append(X2)
                        a3 = F2
                        a4 = X2

                    #else:
                        #print('Not Used')

                    newf.write(line)

        content.close()
        newf.close()

        self.Uy1 = Uy1
        self.Uy2 = Uy2
        self.Fy1 = Fy1
        self.Fy2 = Fy2

    def Uy1(self):
        return self.Uy1
    def Uy2(self):
        return self.Uy2
    def Fy1(self):
        return self.Fy1
    def Fy2(self):
        return self.Fy2


fontpath = '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'
fontprop = fm.FontProperties(family='Arial', fname=fontpath, size=16)
mpl.rcParams.update({'font.size': 16, 'font.family': 'Arial'})

plt.figure(figsize=(11, 5))


