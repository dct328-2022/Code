status = "use"
# status = "try"
# choose "use" or "try"

import copy
import numpy as np
import pandas as pd

ii = 256
jj = 333333
tmax = 3600
InitialTemp = 20
T = np.ones((ii, jj))*InitialTemp
Serie = 1

def LinearInterpolation2D(x1, y1, x2, y2, xi, tol=0.01):
    if abs(x1 - xi) < tol:
        return y1
    elif abs(x2 - xi) < tol:
        return y2
    else:
        k = (y2 - y1) / (x2 - x1)
        yi = k * (xi - x1) + y1
        return yi


def ListLinearInterpolation2D(xlist, ylist, xi, tol=0.01):
    # xlist must be monotonic
    xlength = len(xlist)
    ylength = len(ylist)
    if xlist[1] < xlist[0]:
        case = 1
    else:
        case = 0
    if xlength != ylength:
        print("The lengths of xlist and ylist are not the same!")
    else:
        if xlist[1] >= xlist[0]:
            if xi < xlist[0]:
                yi = LinearInterpolation2D(xlist[0], ylist[0], xlist[1], ylist[1], xi, tol)
            elif xi > xlist[-1]:
                yi = LinearInterpolation2D(xlist[-2], ylist[-2], xlist[-1], ylist[-1], xi, tol)
            else:
                for i in range(1, xlength):
                    if xi >= xlist[i - 1] and xi <= xlist[i]:
                        yi = LinearInterpolation2D(xlist[i - 1], ylist[i - 1], xlist[i], ylist[i], xi, tol)
                        break
        if xlist[1] < xlist[0]:
            if xi > xlist[0]:
                yi = LinearInterpolation2D(xlist[0], ylist[0], xlist[1], ylist[1], xi, tol)
            elif xi < xlist[-1]:
                yi = LinearInterpolation2D(xlist[-2], ylist[-2], xlist[-1], ylist[-1], xi, tol)
            else:
                for i in range(1, xlength):
                    if xi <= xlist[i - 1] and xi >= xlist[i]:
                        yi = LinearInterpolation2D(xlist[i - 1], ylist[i - 1], xlist[i], ylist[i], xi, tol)
                        break
    return yi

def NumberList(Copied):
    numbers = Copied.split()
    EmptyList = []
    for obj in numbers:
        EmptyList.append(float(obj))
    return EmptyList

class FDM1:
    def __init__(self, Name):
        self.Name = Name
        self.AbsoluteZero = -273.15
        self.Layers = []
    def SetAbsoluteZero(self, AbsoluteZero):
        self.AbsoluteZero = AbsoluteZero
    def SetMeshSize(self, ii, jj):
        self.ThicknessLayer = ii
        self.TimePeriod = jj
    def SetInitialTemp(self, InitialTemp):
        self.InitialTemp = InitialTemp
    def SetAmbientTemp(self, AmbientTemp):
        self.AmbientTemp = AmbientTemp
    def SetLayerNumber(self, LayerNumber):
        self.LayerNumber = LayerNumber
    def AddLayer(self, Properties):
        self.Layers.append(Properties)

def FDMT(ts1, pclist1, klist1, thickness1, ts2, pclist2, klist2, thickness2, ts3, pclist3, klist3, thickness3, Ts, Tse, HeatingType):
    # Calling sequence:
    # ts1: temperature sequence for pclist and klist
    # pclist: product of density and specific heat
    # klist: thermal conductivity
    # Ts: a numpy array, first column should be time, second column should be temperature load
    tmax = Ts[-1, 0]
    dt = float(tmax) / jj
    dx = 0.128 / ii
    i1 = int(thickness3/dx)
    i2 = int(thickness1/dx + i1)
    i3 = int(thickness2/dx + i2)
    print(i1, i2, i3)
    dx2 = dx * dx
    print("Kappa should be less than %f" % (dx2 / dt / 2))
    dx1 = 1.0 / dx
    tperiod = jj / 10
    tperiod2 = jj / 100

    if HeatingType == "ConvecRadia":
        IniTmepM = np.zeros((1, jj))

    for j in range(0, jj):
        tempI = ListLinearInterpolation2D(Ts[:, 0], Ts[:, 1], j*dt)
        tempJ = ListLinearInterpolation2D(Tse[:, 0], Tse[:, 1], j*dt)
        
        if HeatingType == "ApplyTemperature":
            T[0, j] = tempI
            T[ii-1, j] = tempJ

    print("ee")
    for j in range(1, jj):
        # Gypsum panel
        for i in range(1, i1):
            k3 = ListLinearInterpolation2D(ts3, klist3, T[i, j - 1])
            pc3 = ListLinearInterpolation2D(ts3, pclist3, T[i, j - 1])
            k4 = ListLinearInterpolation2D(ts3, klist3, T[i - 1, j - 1])
            Tdf1 = T[i + 1, j - 1] - T[i, j - 1]
            Tdf2 = T[i, j - 1] - T[i - 1, j - 1]
            temp = k3*Tdf1*dx1 - k4*Tdf2*dx1
            T[i, j] = T[i, j - 1] + temp*dx1*dt/pc3

        # Transition
        i = i1
        km1 = ListLinearInterpolation2D(ts3, klist3, T[i - 1, j - 1])
        pcm1 = ListLinearInterpolation2D(ts3, pclist3, T[i - 1, j - 1])
        km2 = ListLinearInterpolation2D(ts1, klist1, T[i, j - 1])
        Tdf1 = T[i + 1, j - 1] - T[i, j - 1]
        Tdf2 = T[i, j - 1] - T[i - 1, j - 1]
        temp = km2 * Tdf1 * dx1 - km1 * Tdf2 * dx1
        T[i, j] = T[i, j - 1] + temp * dx1 * dt / pcm1
        
        # First Layer
        for i in range(i1 + 1, i2):
            k2 = ListLinearInterpolation2D(ts1, klist1, T[i, j - 1])
            pc2 = ListLinearInterpolation2D(ts1, pclist1, T[i, j - 1])
            k3 = ListLinearInterpolation2D(ts1, klist1, T[i - 1, j - 1])
            Tdf1 = T[i + 1, j - 1] - T[i, j - 1]
            Tdf2 = T[i, j - 1] - T[i - 1, j - 1]
            temp = k2*Tdf1*dx1 - k3*Tdf2*dx1
            T[i, j] = T[i, j - 1] + temp*dx1*dt/pc2

        # Transition
        i = i2
        km1 = ListLinearInterpolation2D(ts1, klist1, T[i - 1, j - 1])
        pcm1 = ListLinearInterpolation2D(ts1, pclist1, T[i - 1, j - 1])
        km2 = ListLinearInterpolation2D(ts2, klist2, T[i, j - 1])
        Tdf1 = T[i + 1, j - 1] - T[i, j - 1]
        Tdf2 = T[i, j - 1] - T[i - 1, j - 1]
        temp = km2 * Tdf1 * dx1 - km1 * Tdf2 * dx1
        T[i, j] = T[i, j - 1] + temp * dx1 * dt / pcm1

        # Second Layer
        for i in range(i2 + 1, i3):
            k2 = ListLinearInterpolation2D(ts2, klist2, T[i, j - 1])
            pc2 = ListLinearInterpolation2D(ts2, pclist2, T[i, j - 1])
            k3 = ListLinearInterpolation2D(ts2, klist2, T[i - 1, j - 1])
            Tdf1 = T[i + 1, j - 1] - T[i, j - 1]
            Tdf2 = T[i, j - 1] - T[i - 1, j - 1]
            temp = k2 * Tdf1 * dx1 - k3 * Tdf2 * dx1
            T[i, j] = T[i, j - 1] + temp * dx1 * dt / pc2

        # Transition
        i = i3
        km2 = ListLinearInterpolation2D(ts2, klist2, T[i - 1, j - 1])
        pcm2 = ListLinearInterpolation2D(ts2, pclist2, T[i - 1, j - 1])
        km1 = ListLinearInterpolation2D(ts1, klist1, T[i, j - 1])
        Tdf1 = T[i + 1, j - 1] - T[i, j - 1]
        Tdf2 = T[i, j - 1] - T[i - 1, j - 1]
        temp = km1 * Tdf1 * dx1 - km2 * Tdf2 * dx1
        T[i, j] = T[i, j - 1] + temp * dx1 * dt / pcm2

        # Third Layer
        for i in range(i3 + 1, ii - 1):
            k2 = ListLinearInterpolation2D(ts1, klist1, T[i, j - 1])
            pc2 = ListLinearInterpolation2D(ts1, pclist1, T[i, j - 1])
            k3 = ListLinearInterpolation2D(ts1, klist1, T[i - 1, j - 1])
            Tdf1 = T[i + 1, j - 1] - T[i, j - 1]
            Tdf2 = T[i, j - 1] - T[i - 1, j - 1]
            temp = k2 * Tdf1 * dx1 - k3 * Tdf2 * dx1
            T[i, j] = T[i, j - 1] + temp * dx1 * dt / pc2


# Data for GFRP panel
ts1 = "0	5	10	15	20	25	30	35	40	45	50	55	60	65	70	75	80	85	90	95	100	105	110	115	120	125	130	135	140	145	150	155	160	165	170	175	180	185	190	195	200	205	210	215	220	225	230	235	240	245	250	255	260	265	270	275	280	285	290	295	300	305	310	315	320	325	330	335	340	345	350	355	360	365	370	375	380	385	390	395	400	405	410	415	420	425	430	435	440	445	450	455	460	465	470	475	480	485	490	495	500	505	510	515	520	525	530	535	540	545	550	555	560	565	570	575	580	585	590	595	600	900"
pclist1 = "1706.064146	1708.103833	1710.143269	1712.182457	1714.221395	1716.260085	1718.309148	1720.566657	1722.823891	1725.08085	1727.337534	1729.593944	1732.129104	1734.813849	1737.316768	1739.721417	1742.067023	1743.773069	1745.478201	1747.18242	1748.885725	1750.711187	1752.633	1754.30598	1755.976865	1757.647406	1759.317604	1760.98746	1762.656972	1764.290605	1766.317081	1768.341796	1770.364752	1772.385949	1777.292836	1791.943276	1806.575865	1827.729626	1854.926122	1887.666292	1931.899891	1972.706991	2012.029011	2096.150553	2199.694066	2301.463702	2395.968503	2482.800586	2550.902965	2542.306803	2512.107292	2408.060721	2279.375878	2107.849514	2031.963608	2044.242	2072.787152	2149.913279	2225.003713	2401.894333	2565.11436	2740.020304	2972.236238	3144.812603	3409.003821	3691.964999	3967.738142	4295.248975	4586.236243	4867.41005	5134.720158	5203.759291	5042.980681	4515.798532	3750.999441	2917.099066	2275.759429	1935.964498	1750.768087	1645.479672	1583.065954	1542.934172	1525.065792	1499.535492	1464.627408	1444.522938	1449.164772	1449.796324	1455.247418	1475.231532	1500.294875	1523.12223	1537.094842	1555.104363	1575.245717	1597.572561	1628.283823	1630.907689	1626.616265	1626.479794	1613.057795	1540.794006	1446.770781	1360.213965	1258.119444	1163.299252	1076.388127	1043.532889	1018.539463	993.2065157	977.9531306	972.3754436	966.8003063	962.5090886	959.6417799	956.775385	955.0698503	954.9084722	954.747094	954.5857158	954.4243349	954.4243349"
klist1 = "0.317714	0.317714	0.317714	0.317714	0.317714	0.317714	0.317698321	0.31738208	0.317065839	0.316749597	0.316433356	0.316117115	0.315800874	0.315484633	0.315126711	0.314759892	0.314393072	0.314026252	0.313673098	0.313398143	0.313123189	0.312848234	0.31257328	0.312298326	0.312023371	0.31165407	0.311276004	0.310897938	0.310519872	0.310124061	0.30969947	0.309274878	0.308715167	0.308094578	0.307430114	0.306658545	0.305313997	0.303969641	0.302625524	0.300915798	0.298920821	0.296323261	0.293394706	0.289779951	0.284884123	0.280538504	0.274305987	0.267987175	0.261648564	0.255789169	0.249785886	0.245268224	0.242042041	0.239202859	0.237091705	0.234671728	0.231763911	0.228385596	0.224738981	0.220113353	0.215571525	0.208641032	0.202210779	0.194816943	0.187292488	0.179561312	0.170490884	0.160810854	0.151514587	0.14251741	0.133926086	0.125660722	0.118685778	0.113253363	0.109533396	0.107357478	0.106052005	0.104981688	0.10421862	0.103455552	0.102692485	0.101929417	0.10116635	0.100708552	0.10026039	0.099812228	0.099364067	0.098915905	0.098467743	0.097907532	0.097270672	0.096633812	0.095996952	0.095360092	0.094693013	0.093912389	0.093131765	0.092351141	0.091570517	0.090907521	0.090270661	0.089675085	0.089364845	0.089066366	0.088797451	0.088539257	0.088337605	0.088135954	0.088	0.088	0.088	0.088	0.088	0.088	0.088	0.088	0.088	0.088	0.088	0.088	0.088	0.088"
ts1 = NumberList(ts1)
pclist1 = NumberList(pclist1)
klist1 = NumberList(klist1)
pclist1 = list(map(lambda xx: xx*1000, pclist1))

# Data for middle layer
ts2 = "0	19.9	29.9	39.9	49.9	59.9	69.9	79.9	89.9	99.9	109.9	119.9	129.9	139.9	149.9	159.9	169.9	179.9	189.9	199.9	209.9	219.9	229.9	239.9	249.9	259.9	269.9	279.9	289.9	299.9	309.9	319.9	329.9	339.9	349.9	359.9	369.9	379.9	389.9	399.9	409.9	419.9	429.9	439.9	449.9	459.9	469.9	479.9	489.9	499.9	509.9	519.9	529.9	539.9	549.9	559.9	569.9	579.9	589.9	599.9	609.9	619.9	629.9	639.9	649.9	659.9	669.9	679.9	689.9	699.9	709.9	719.9	729.9	739.9	749.9	759.9	769.9	779.9	789.9	799.9	809.9	819.9	829.9	839.9	849.9	859.9	869.9	879.9	889.9	899.9	909.9	919.9	929.9	939.9	949.9	959.9	969.9	979.9	989.9	999.9	1009.9	1019.9"
pclist2 = "300	300	300	380	460	540	620	700	780	860	780	700	620	540	460	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380	380"
klist2 = "2.4	2.4	2.4	2.40236686	2.40946744	2.42130174	2.43786976	2.4591715	2.48520696	2.51597614	2.55147904	2.59171566	2.636686	2.68639006	2.74082784	2.79999934	2.8	2.802	2.804	2.806	2.808	2.81	2.812	2.814	2.816	2.818	2.82	2.822	2.824	2.826	2.828	2.83	2.832	2.834	2.836	2.838	2.84	2.842	2.844	2.846	2.848	2.85	2.852	2.854	2.856	2.858	2.86	2.862	2.864	2.866	2.868	2.87	2.872	2.874	2.876	2.878	2.88	2.882	2.884	2.886	2.888	2.89	2.892	2.894	2.896	2.898	2.9	2.902	2.904	2.906	2.908	2.91	2.912	2.914	2.916	2.918	2.92	2.922	2.924	2.926	2.928	2.93	2.932	2.934	2.936	2.938	2.94	2.942	2.944	2.946	2.948	2.95	2.952	2.954	2.956	2.958	2.96	2.962	2.964	2.966	2.968	2.97"
ts2 = NumberList(ts2)
pclist2 = NumberList(pclist2)
klist2 = NumberList(klist2)
pclist2 = list(map(lambda xx: xx*1000, pclist2))

# For test only
'''ts1 = [0, 3600, 7200]
pclist1 = [500, 500, 500]
klist1 = [0.3, 0.3, 0.3]
pclist1 = list(map(lambda xx: xx*1000, pclist1))'''

# Data for Gypsum
ts3 = "0	10	20	30	40	50	60	70	80	90	100	110	120	130	140	150	160	170	180	190	200	210	220	230	240	250	260	270	280	290	300	310	320	330	340	350	360	370	380	390	400	410	420	430	440	450	460	470	480	490	500	510	520	530	540	550	560	570	580	590	600	610	620	630	640	650	660	670	680	690	700	710	720	730	740	750	760	770	780	790	800	810	820	830	840	850	860	870	880	890	900	910	920	930	940	950	960	970	980	990	1000"
klist3 = "0.25	0.25	0.25	0.25	0.25	0.25	0.25	0.25	0.25	0.25	0.25	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.12	0.221	0.2245	0.228	0.2315	0.235	0.2385	0.242	0.2455	0.249	0.2525	0.256	0.2595	0.263	0.2665	0.27	0.283	0.296	0.309	0.322	0.335	0.348	0.361	0.374	0.387	0.4	2.32	4.24	6.16	8.08	10	10	10	10	10	10"
pclist3 = "680	680	680	680	680	680	680	680	680	2264.4	5440	8249.437	10788.948	13058.533	8466	4515.2	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	564.4	747.9388	930.1312	1110.9772	1290.4768	1468.63	1645.4368	1375.3	1096.16	819.06	544	544	544	544	544	544	544	544	544	544	544	544	544	544	544	544	544	544	544	544	544	348.3558672	196.1338688	87.3340048	21.9562752	0.00068	0.00068	0.00068	0.00068	0.00068	0.00068"
ts3 = NumberList(ts3)
pclist3 = NumberList(pclist3)
klist3 = NumberList(klist3)
pclist3 = list(map(lambda xx: xx*1000, pclist3))


# Begin and End numbers
GroupNBegin = 2279
GroupNEnd = 2299
#GroupNEnd = 3791
GroupPBegin = 4414
GroupPEnd = 4434
#GroupPEnd = 5926

# Loading temperature
fn = '204woGyp_devc.csv'
df = pd.read_csv(fn, header=1)

def SearchIndex(xx):
    for i, obj in enumerate(df.keys()):
        if obj != 'Time':
            if int(obj) == xx:
                return i

NodePairFile = open("NodePairs%d.txt"%Serie, 'r')
NodePair = []
NodePairIndex1 = []
NodePairIndex2 = []
for line in NodePairFile:
    split = line.split()
    if len(split) == 2:
        NodePair.append([int(split[0]), int(split[1])])
        temp1 = SearchIndex(int(split[0]))
        temp2 = SearchIndex(int(split[1]))
        NodePairIndex1.append(temp1)
        NodePairIndex2.append(temp2)
    else:
        print("NodePair cannot be found")

fn2 = open("CalResultsStage2-%d.txt"%Serie, 'w')
TsTime = df.iloc[:, 0].values
for i, num in enumerate(NodePairIndex1):
    if num < 1974:
        continue
    num2 = NodePairIndex2[i]
    fn2.write("%d" % num)
    Temp = df.iloc[:, num].values
    Temp2 = df.iloc[:, num2].values
    if Temp2[-1] > 900:
        fn2.write("Temperature too high\n")
        T = np.ones((ii, jj))*InitialTemp
        print("Temperature is too high")
        continue
    Ts = np.stack((TsTime,Temp))
    Tse = np.stack((TsTime,Temp2))
    Ts = np.transpose(Ts)
    Tse = np.transpose(Tse)

    print("Begin %d and %d" % (num, num2))
    FDMT(ts1, pclist1, klist1, 0.008, ts2, pclist2, klist2, 0.1, ts3, pclist3, klist3, 0.012, Ts, Tse, "ApplyTemperature")
    dx = 0.128 / ii
    i1 = int(0.012/dx)
    for iter in range(0, jj):
        fn2.write(" %f" % T[i1, iter])
    fn2.write("\n")
    T = np.ones((ii, jj))*InitialTemp
    

    
