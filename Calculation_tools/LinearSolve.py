from sympy import *
import gmpy2
from gmpy2 import mpfr
def LinearSolve(a1,n,b1,cc):
    TINY=mpfr(1e-20)
    indx=zeros(1,n)
    vv=zeros(1,n)
    d=1.0;
    a=[[0 for x in range(n)] for x in range(n)]
    b=[0 for x in range(n)]
    for i in range(0,n):
        for j in range(0,n):
            a[i][j]=mpfr(float(a1[i,j]))
        b[i]=mpfr(float(b1[i]))
    for i in range(0,n):
        big=0.0;
        for j in range(0,n):
            if a[i][j]>=0:
                temp=a[i][j];
            else:
                temp=-a[i][j];
            if temp>big:
                big=temp;
        if big==0:
            print("===========ERROR==============")
    for j in range(0,n):
        for i in range(0,j):
            sum1=a[i][j];
            for k in range(0,i):
                sum1 =sum1-a[i][k]*a[k][j]
            a[i][j]=sum1
        big=0.0;
        for i in range(j,n):
            sum1=a[i][j];
            for k in range(0,j):
                sum1 =sum1- a[i][k]*a[k][j];
            a[i][j]=sum1;
            dum=vv[i]*abs(sum1);
            if dum>=big:
                big=dum;
                imax=i;
        if j!=imax:
            for k in range(0,n):
                dum=a[imax][k];
                a[imax][k]=a[j][k];
                a[j][k]=dum;
            d=-d;
            vv[imax]=vv[j];
        indx[j]=imax;
        if a[j][j]==0:
            a[j][j]=TINY;
        if j!= n-1:
            dum=1.0/a[j][j];
            for i in range(j+1,n):
                a[i][j]=a[i][j]*dum;
    for i in range(0,n):
        vv[i]=0.0;
    sum1=0.0;
    ii=0.0
    for i in range(0,n):
        ip=indx[i];
        sum1=b[ip];
        b[ip]=b[i];
        if ii!=0:
            for j in range(ii-1,i):
                sum1=sum1-a[i][j]*b[j];
        elif abs(sum1)>1e-18:
            ii=i+1;
        b[i]=sum1;
    i=n-1
    while(i>=0):
        sum1=b[i];
        for j in range(i+1,n):
            sum1 =sum1-a[i][j]*b[j];
        b[i]=float(sum1/a[i][i]);
        i=i-1
    replacements=[(cc[i],b[i]) for i in range(0,n)]
    return replacements
c=symbols('c0:4')
A=Matrix([[1,2,0,5],[3,2,2,-2],[2,0,0,-8],[2,6,1,8]])
B=Matrix([1,1,1,-3])
cc=LinearSolve(A,4,B,c)
print(cc)
A=SparseMatrix([[1,2,0,5],[3,2,2,-2],[2,0,0,-8],[2,6,1,8]])
B=SparseMatrix([1,1,1,-3])
xy=A.solve(B,method='LDL')
print('xy=',xy.evalf())
print(A*xy-B)