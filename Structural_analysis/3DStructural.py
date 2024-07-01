import xlrd
import xlwt
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from scipy import linalg
from numpy.linalg import solve, norm
from numpy.random import rand
from sympy import *
## Determine the length, oriantation,axial stiffness,bending stiffness of each elements/com
## l(:,0):length,l(:,1):EA, l(:,2):EIy, l(:,3):EIz, l(:,4):GIp,4,5,6,7
##l[:,5]:x2-x1, l[:,6]:y2-y1, l[:,7]:z2-z1, l[:,8]:x3-x1, l[:,9]:y3-y1, l[:,10]:z3-z1, l[:,11]:x3-x2, l[:,12]:y3-y2, l[:,13]:z3-z2
def lengthangle(ne):
    global XY,NE,x
    l=zeros(ne,14)
    for u in range(0,ne):
        VE=XY[NE[u,1]-1,:]-XY[NE[u,0]-1,:]
        l[u,0]=(VE[0]**2+VE[1]**2+VE[2]**2)**(1/2) #length
        l[u,1]=NE[u,6]*NE[u,7] #EA
        l[u,2]=NE[u,6]*NE[u,8] #EIy
        l[u,3]=NE[u,6]*NE[u,9] #EIz
        l[u,4]=NE[u,6]*NE[u,10]/(2*(1+NE[u,11])) #GIp
        #2-1
        l[u,5]=XY[NE[u,1]-1,0]-XY[NE[u,0]-1,0]
        l[u,6]=XY[NE[u,1]-1,1]-XY[NE[u,0]-1,1]
        l[u,7]=XY[NE[u,1]-1,2]-XY[NE[u,0]-1,2]
        #3-1
        l[u,8]=NE[u,2]-XY[NE[u,0]-1,0]
        l[u,9]=NE[u,3]-XY[NE[u,0]-1,1]
        l[u,10]=NE[u,4]-XY[NE[u,0]-1,2]
        #3-2
        l[u,11]=NE[u,2]-XY[NE[u,1]-1,0]
        l[u,12]=NE[u,3]-XY[NE[u,1]-1,1]
        l[u,13]=NE[u,4]-XY[NE[u,1]-1,2]
    return l;

def rotm(ne,l):
    global XY,NE,x
    rotma1=[]
    for u in range(0,ne):
        t1 = l[u, 11]
        t2 = t1**2
        t3 = l[u, 8]
        t6 = l[u, 13]
        t7 = t6**2
        t8 = l[u, 10]
        t11 = t8**2
        t12 = l[u, 12]
        t13 = t12**2
        t14 = l[u, 9]
        t17 = t14**2
        t18 = t3**2
        t20 = (-2*t1*t3-2*t12*t14-2*t6*t8+t11+t13+t17+t18+t2+t7)**(1/2)
        t21 = 1/t20
        t31 = t12-t14
        t34 = -t1*t14+t12*t3
        t36 = -t6+t8
        t39 = t1*t8-t3*t6
        t41 = t31*t34+t36*t39
        t42 = t41**2
        t43 = -t1+t3
        t47 = -t12*t8+t14*t6
        t49 = t34*t43-t36*t47
        t50 = t49**2
        t53 = -t31*t47-t39*t43
        t54 = t53**2
        t56 = sqrt(t42+t50+t54)
        t57 = 1/t56
        t61 = t34**2
        t62 = t39**2
        t63 = t47**2
        t65 = sqrt(t61+t62+t63)
        t66 = 1/t65
        rotma1.insert(u,Matrix([[-t1*t21+t21*t3,-t12*t21+t14*t21,-t21*t6+t21*t8],[t41*t57,t49*t57,t53*t57],[t47*t66,t39*t66,t34*t66]]))
    return rotma1

 
##Generate axial differential equations, unknowns are c[u][5] and c[u][6];com
## In the returned Matrix, the first column is displacement, the second is column is axial force;
def AxialDiff(l,ne):
    global XY,NE,Pu,x,c,i,rotma,Axialcoe;
    Axialeqn=zeros(ne,2);
    Axialcoe=[]
    tem=0;
    for u in range(0,ne):
        pgt=-NE[u,5]*rotma[u][0,2]
        if NE[u,7]==inf:
            Axialeqn[u,1]=-(pgt+Pu[u,0])*x+c[i]
            Axialeqn[u,0]=c[i+1]
            Axialcoe.insert(tem,[i+1])
            tem=tem+1
            Axialcoe.insert(tem,[i])
            tem=tem+1
        else:
            Axialeqn[u,0]=integrate(integrate(-(pgt+Pu[u,0])/l[u,1],x),x)+c[i]*x+c[i+1]
            Axialeqn[u,1]=l[u,1]*Axialeqn[u,0].diff(x)
            Axialcoe.insert(tem,[i,i+1])
            tem=tem+1
            Axialcoe.insert(tem,[i])
            tem=tem+1
        i=i+2
    return Axialeqn;

##Generate lateral differential equations with constant unknowns c[u][1]..c[u][4]
##In the returned matrix, the first column is displacement, the second is oriantation, the third is Moment, the fourth is ShearForce
def LateralDiffy(l,ne):
    global XY,NE,Pu,x,c,i,rotma,Lateralycoe;
    Lateraleqn=zeros(ne,4);
    Lateralycoe=[];
    tem=0;
    for u in range(0,ne):
        if NE[u,9]==inf:
            Lateraleqn[u,0]=c[i]*x+c[i+1]
            Lateraleqn[u,1]=c[i]
            Lateraleqn[u,2]=c[i+2]*x+c[i+3]+(Pu[u,1]-NE[u,5]*rotma[u][1,2])*l[u,0]*x/2-(Pu[u,1]-NE[u,5]*rotma[u][1,2])*x**2/2
            Lateraleqn[u,3]=-Lateraleqn[u,2].diff(x)
            Lateralycoe.insert(tem,[i,i+1])
            tem=tem+1
            Lateralycoe.insert(tem,[i])
            tem=tem+1
            Lateralycoe.insert(tem,[i+2,i+3])
            tem=tem+1
            Lateralycoe.insert(tem,[i+2])
            tem=tem+1
        else:    
            G=NE[u,6]/(2*(1+NE[u,11]))
            Lateraleqn[u,0]=integrate((integrate((integrate(-(NE[u,5]*rotma[u][1,2]*NE[u,7]*G-Pu[u,1]*G*NE[u,7]-NE[u,13]*(diff(Pu[u,2],x,2))*l[u,3])/(l[u,3]*G*NE[u,7]),x,x)+c[i]*x),x)+c[i+1]*x),x)+c[i+2]*x+c[i+3];
            f1=diff(Lateraleqn[u,0],x)
            Lateraleqn[u,1]=f1+NE[u,13]*l[u,3]*diff(f1,x,2)/(G*NE[u,7])
            Lateraleqn[u,2]=-l[u,3]*diff(Lateraleqn[u,1],x)
            Lateraleqn[u,3]=-diff(Lateraleqn[u,2],x)
            Lateralycoe.insert(tem,[i,i+1,i+2,i+3])
            tem=tem+1
            Lateralycoe.insert(tem,[i,i+1,i+2])
            tem=tem+1
            Lateralycoe.insert(tem,[i,i+1])
            tem=tem+1
            Lateralycoe.insert(tem,[i])
            tem=tem+1
        i=i+4
    return Lateraleqn

##Generate lateral differential equations with constant unknowns c[u][1]..c[u][4]
##In the returned matrix, the first column is displacement, the second is oriantation, the third is Moment, the fourth is ShearForce
def LateralDiffz(l,ne):
    global XY,NE,Pu,x,y1,c,i,rotma,Lateralzcoe;
    Lateraleqn=zeros(ne,4);
    Lateralzcoe=[];
    tem=0
    for u in range(0,ne):
        if NE[u,8]==inf:
            Lateraleqn[u,0]=c[i]*x+c[i+1]
            Lateraleqn[u,1]=c[i]
            Lateraleqn[u,2]=c[i+2]*x+c[i+3]+(Pu[u,2]-NE[u,5]*rotma[u][2,2])*l[u,0]*x/2-(Pu[u,2]-NE[u,5]*rotma[u][2,2])*x**2/2
            Lateraleqn[u,3]=-Lateraleqn[u,2].diff(x)
            Lateralzcoe.insert(tem,[i,i+1])
            tem=tem+1
            Lateralzcoe.insert(tem,[i])
            tem=tem+1
            Lateralzcoe.insert(tem,[i+2,i+3])
            tem=tem+1
            Lateralzcoe.insert(tem,[i+2])
            tem=tem+1
        else:
            G=NE[u,6]/(2*(1+NE[u,11]))
            Lateraleqn[u,0]=integrate((integrate((integrate(-(NE[u,5]*rotma[u][2,2]*NE[u,7]*G-Pu[u,2]*G*NE[u,7]-NE[u,12]*(diff(Pu[u,1],x,2))*l[u,2])/(l[u,2]*G*NE[u,7]),x,x)+c[i]*x),x)+c[i+1]*x),x)+c[i+2]*x+c[i+3];
            f1=diff(Lateraleqn[u,0],x)
            Lateraleqn[u,1]=f1+NE[u,12]*l[u,2]*diff(f1,x,2)/(G*NE[u,7])
            Lateraleqn[u,2]=-l[u,2]*diff(Lateraleqn[u,1],x)
            Lateraleqn[u,3]=-diff(Lateraleqn[u,2],x)
            Lateralzcoe.insert(tem,[i,i+1,i+2,i+3])
            tem=tem+1
            Lateralzcoe.insert(tem,[i,i+1,i+2])
            tem=tem+1
            Lateralzcoe.insert(tem,[i,i+1])
            tem=tem+1
            Lateralzcoe.insert(tem,[i])
            tem=tem+1
        i=i+4
    return Lateraleqn

def Torque(l,ne):
    global XY,NE,Pu,x,y1,c,i,Torquecoe;
    Torqueeqn=zeros(ne,2)
    Torquecoe=[]
    tem=0
    for u in range(0,ne):
        if NE[u,10]==inf:
            Torqueeqn[u,0]=c[i]
            Torqueeqn[u,1]=c[i+1]
            Torquecoe.insert(tem,[i])
            tem=tem+1
            Torquecoe.insert(tem,[i+1])
            tem=tem+1
        else:
            Torqueeqn[u,0]=(c[i]*x+c[i+1])
            Torqueeqn[u,1]=l[u,4]*Torqueeqn[u,0].diff(x)
            Torquecoe.insert(tem,[i,i+1])
            tem=tem+1
            Torquecoe.insert(tem,[i])
            tem=tem+1
        i=i+2
    return Torqueeqn;
    
def Force(ne,l,Axialeqn,Lateraleqny,Lateraleqnz,Torqueeqn):
    global XY,NE,x,c,rotma,oforcecoe;
    oforce=[];
    oforcecoe=[]
    for u in range(0,ne):
        rm=rotma[u]
        rmn=rm**(-1)
        fr1=Matrix([[Axialeqn[u,0].subs(x,0),Axialeqn[u,0].subs(x,l[u,0]),-Axialeqn[u,1].subs(x,0),Axialeqn[u,1].subs(x,l[u,0])],[Lateraleqny[u,0].subs(x,0),Lateraleqny[u,0].subs(x,l[u,0]),Lateraleqny[u,3].subs(x,0),-Lateraleqny[u,3].subs(x,l[u,0])],[Lateraleqnz[u,0].subs(x,0),Lateraleqnz[u,0].subs(x,l[u,0]),Lateraleqnz[u,3].subs(x,0),-Lateraleqnz[u,3].subs(x,l[u,0])]]);
        fr2=Matrix([[Torqueeqn[u,0].subs(x,0),Torqueeqn[u,0].subs(x,l[u,0]),Torqueeqn[u,1].subs(x,0),-Torqueeqn[u,1].subs(x,l[u,0])],[-Lateraleqnz[u,1].subs(x,0),-Lateraleqnz[u,1].subs(x,l[u,0]),Lateraleqnz[u,2].subs(x,0),-Lateraleqnz[u,2].subs(x,l[u,0])],[Lateraleqny[u,1].subs(x,0),Lateraleqny[u,1].subs(x,l[u,0]),-Lateraleqny[u,2].subs(x,0),Lateraleqny[u,2].subs(x,l[u,0])]]);
        forc1=rmn*fr1;
        forc2=rmn*fr2;
        forc=forc1.col_join(forc2)
        oforce.insert(u,Matrix(forc));
        oforceb={0}
        jihe=Axialcoe[2*u]+Axialcoe[2*u]+Axialcoe[2*u+1]+Axialcoe[2*u+1]+Lateralycoe[4*u]+Lateralycoe[4*u]+Lateralycoe[4*u+3]+Lateralycoe[4*u+3]+Lateralzcoe[4*u]+Lateralzcoe[4*u]+Lateralzcoe[4*u+3]+Lateralzcoe[4*u+3],Torquecoe[2*u]+Torquecoe[2*u]+Torquecoe[2*u+1]+Torquecoe[2*u+1]+Lateralzcoe[4*u+1]+Lateralzcoe[4*u+1]+Lateralzcoe[4*u+2]+Lateralzcoe[4*u+2]+Lateralycoe[4*u+1]+Lateralycoe[4*u+1]+Lateralycoe[4*u+2]+Lateralycoe[4*u+2]
        for u2 in jihe:
            oforceb=oforceb.union(u2)
        oforcecoe.insert(u,oforceb)
    return oforce;

def findele(u3,ne):
    global XY,NE,x;
    rel1=zeros(0,0);
    rel2=zeros(0,0);
    n1=0;
    n2=0;
    for u in range(0,ne):
        if NE[u,0]==u3:
            n1=n1+1
            if n1==1:
                rel1=zeros(1,1);
                rel1[0,0]=u+1
            else:
                rel1=rel1.col_insert(n1,Matrix([u+1]))
        if NE[u,1]==u3:
            n2=n2+1
            if n2==1:
                rel2=zeros(1,1);
                rel2[0,0]=u+1
            else:
                rel2=rel2.col_insert(n2,Matrix([u+1]))
    if rel1.shape==(0,0):
        rel=rel2
        rel=rel.col_join(zeros(1,n2))
    elif rel2.shape==(0,0):
        rel=rel1
        rel=rel.col_join(-ones(1,n1))
    else:
        rel=rel1.row_join(rel2)
        rel3=(-ones(1,n1)).row_join(zeros(1,n2))
        rel=rel.col_join(rel3)
    return rel;

def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6
    style.font = font
    # style.borders = borders
    return style



def fMaxMin(f,x,a,b):
    e1=f.subs(x,a).evalf()
    e2=f.subs(x,b).evalf()
    if e1>=e2:
        mi=e2
        ma=e1
        po2=b
        po1=a
    elif e1<e2:
        mi=e1
        ma=e2
        po2=a
        po1=b
    df=diff(f,x)
    sol=solve(df,x)
    nos=len(sol)
    for u in range(0,nos):
        if abs(im(sol[u]).evalf())<1e-12:
            if re(sol[u]).evalf()>a and re(sol[u]).evalf()<b:
                t=f.subs(x,re(sol[u])).evalf()
                if t<mi:
                    mi=t
                    po2=re(sol[u]).evalf()
                if t>ma:
                    ma=t
                    po1=re(sol[u]).evalf()
    return (ma,po1,mi,po2)

print('Welcome to use Structural Solver')
x=Symbol('x')
free=Symbol('free')
inf=Symbol('inf')
xlsfile=xlrd.open_workbook("D:\\PyProgram\\3DStructuralSolver.xlsx")
mysheet=xlsfile.sheet_by_name("Sheet1")
nrow1=mysheet.nrows
ncol1=mysheet.ncols
u1=4
u2=1
XY=zeros(0,3)
while u1<nrow1:
    if(mysheet.cell_value(u1,u2)!=''):
        XY=XY.row_insert(u1-4,zeros(1,3))
        XY[u1-4,u2-1]=mysheet.cell_value(u1,u2)
        XY[u1-4,u2]=mysheet.cell_value(u1,u2+1)
        XY[u1-4,u2+1]=mysheet.cell_value(u1,u2+2)
    u1=u1+1
rowcol=XY.shape
xy=rowcol[0]
u1=4
u2=19
NE=zeros(0,14)
while u1<nrow1:
    if(mysheet.cell_value(u1,u2)!=''):
        NE=NE.row_insert(u1-4,zeros(1,14))
        NE[u1-4,u2-19]=int(mysheet.cell_value(u1,u2)) #1
        NE[u1-4,u2-18]=int(mysheet.cell_value(u1,u2+1)) #2
        NE[u1-4,u2-17]=simplify(mysheet.cell_value(u1,u2+2)) #x
        NE[u1-4,u2-16]=simplify(mysheet.cell_value(u1,u2+3)) #y
        NE[u1-4,u2-15]=simplify(mysheet.cell_value(u1,u2+4)) #z
        NE[u1-4,u2-14]=simplify(mysheet.cell_value(u1,u2+5)) #pg
        NE[u1-4,u2-13]=simplify(mysheet.cell_value(u1,u2+6)) #E
        NE[u1-4,u2-12]=simplify(mysheet.cell_value(u1,u2+7)) #A
        NE[u1-4,u2-11]=simplify(mysheet.cell_value(u1,u2+8)) #Iy
        NE[u1-4,u2-10]=simplify(mysheet.cell_value(u1,u2+9)) #Iz
        NE[u1-4,u2-9]=simplify(mysheet.cell_value(u1,u2+10))  #Ip
        NE[u1-4,u2-8]=simplify(mysheet.cell_value(u1,u2+11)) #u
        NE[u1-4,u2-7]=mysheet.cell_value(u1,u2+12) #ky
        NE[u1-4,u2-6]=mysheet.cell_value(u1,u2+13) #kz
    u1=u1+1
rowcol=NE.shape
ne=rowcol[0]
cnumbers=12*ne
c=symbols('c0:%d'%cnumbers)
eq=zeros(1,cnumbers)
eq=list(eq)
eqcoe=zeros(1,cnumbers)
Pu=zeros(ne,3)
u1=4
u2=33
while u1<4+ne:
    if(mysheet.cell_value(u1,u2)==''):
        Pu[u1-4,u2-33]=0
    if(mysheet.cell_value(u1,u2+1)==''):
        Pu[u1-4,u2-32]=0
    if(mysheet.cell_value(u1,u2+2)==''):
        Pu[u1-4,u2-31]=0
    Pu[u1-4,u2-33]=simplify(mysheet.cell_value(u1,u2))
    Pu[u1-4,u2-32]=simplify(mysheet.cell_value(u1,u2+1))
    Pu[u1-4,u2-31]=simplify(mysheet.cell_value(u1,u2+2))
    u1=u1+1
l=lengthangle(ne)
rotma=rotm(ne,l)
i=0
Axialeqn=AxialDiff(l,ne)
Lateraleqnz=LateralDiffz(l,ne)
Lateraleqny=LateralDiffy(l,ne)
Torqueeqn=Torque(l,ne)
Oforce=Force(ne,l,Axialeqn,Lateraleqny,Lateraleqnz,Torqueeqn);
relea=ones(2*ne,6)
u1=4
u2=36
u3=0
while u1<4+ne:
    relea[u3,u2-36]=simplify(mysheet.cell_value(u1,u2))
    relea[u3,u2-35]=simplify(mysheet.cell_value(u1,u2+1))
    relea[u3,u2-34]=simplify(mysheet.cell_value(u1,u2+2))
    relea[u3,u2-33]=simplify(mysheet.cell_value(u1,u2+3))
    relea[u3,u2-32]=simplify(mysheet.cell_value(u1,u2+4))
    relea[u3,u2-31]=simplify(mysheet.cell_value(u1,u2+5))
    relea[u3+1,u2-36]=simplify(mysheet.cell_value(u1,u2+6))
    relea[u3+1,u2-35]=simplify(mysheet.cell_value(u1,u2+7))
    relea[u3+1,u2-34]=simplify(mysheet.cell_value(u1,u2+8))
    relea[u3+1,u2-33]=simplify(mysheet.cell_value(u1,u2+9))
    relea[u3+1,u2-32]=simplify(mysheet.cell_value(u1,u2+10))
    relea[u3+1,u2-31]=simplify(mysheet.cell_value(u1,u2+11))
    u1=u1+1
    u3=u3+2
Rem=relea.T
u1=4
u2=11
RelM=zeros(xy,6)
while u1<4+xy:
    u2=11
    while u2<17:
        if mysheet.cell_value(u1,u2)=='':
            RelM[u1-4,u2-11]='free'
        else:
            RelM[u1-4,u2-11]=mysheet.cell_value(u1,u2)
        u2=u2+1;
    u1=u1+1;
Cons=RelM.T
u1=4
u2=5
uu2=u2
RelM=zeros(xy,6)
while u1<4+xy:
    u2=uu2
    while u2<11:
        if u2==uu2+2:
            if mysheet.cell_value(u1,u2)=='':
                if mysheet.cell_value(u1,u2-3)=='':
                    RelM[u1-uu2+1,u2-uu2]=0;
                else:
                    RelM[u1-uu2+1,u2-uu2]=-simplify(mysheet.cell_value(u1,u2-3))
            else:
                if mysheet.cell_value(u1,u2-3)=='':
                    RelM[u1-uu2+1,u2-uu2]=simplify(mysheet.cell_value(u1,u2));
                else:
                    RelM[u1-uu2+1,u2-uu2]=simplify(mysheet.cell_value(u1,u2)-mysheet.cell_value(u1,u2-3))   
        else:
            if mysheet.cell_value(u1,u2)=='':
                RelM[u1-uu2+1,u2-uu2]=0;
            else:
                RelM[u1-uu2+1,u2-uu2]=simplify(mysheet.cell_value(u1,u2));
        u2=u2+1
    u1=u1+1;
CP=RelM.T
nj=0
#begin to generate equations
print("begin to generate equations")
from giacpy import simplify
for u in range(0,xy):
    print('u=',u)
    rel=findele(u+1,ne)
    n1=rel.shape[1]
    if n1!=1:
        for u1 in range(0,n1-1):
            t1=2*rel[0,0]+rel[1,0]-1
            if (Rem[0,t1]==1 and Rem[1,t1]==1 and Rem[2,t1]==1 and Rem[3,t1]==1 and Rem[4,t1]==1 and Rem[5,t1]==1):
                break;
            else:
                print("before change",rel)
                rel=rel.row_join(zeros(2,1))
                rel[:,-1]=rel[:,0];
                rel.col_del(0)
                print("change",rel);
        if u1==n1:
            print("!!!You must make one element not released");
        for u1 in range(1,n1):
            for u2 in range(0,6):
                if Rem[u2,2*rel[0,u1]+rel[1,u1]-1]==1:
                    print(u+1,rel[0,u1],u2+1,"not released");
                    ## 1st(rel(2,u1)=-1) or 2nd(rel(2,u1)=0) column
                    nj=nj+1;
                    #eq[nj-1]=simplify(Oforce[rel[0,0]-1][u2,rel[1,0]+1]-Oforce[rel[0,u1]-1][u2,rel[1,u1]+1])
                    eq[nj-1]=Oforce[rel[0,0]-1][u2,rel[1,0]+1]-Oforce[rel[0,u1]-1][u2,rel[1,u1]+1]
                    eq[nj-1]=simplify(eq[nj-1])
                    eqcoe[nj-1]=oforcecoe[rel[0,0]-1].union(oforcecoe[rel[0,u1]-1])
                elif Rem[u2,2*rel[0,u1]+rel[1,u1]-1]==0:
                    print(u+1,rel[0,u1],u2+1,"released");
                    ## 3rd(rel(2,u1)=-1) or 4th(rel(2,u1)=0) column
                    nj=nj+1;
                    eq[nj-1]=simplify(Oforce[rel[0,u1]-1][u2,rel[1,u1]+3]);
                    eqcoe[nj-1]=oforcecoe[rel[0,u1]-1]
    for u1 in range(0,6):
        if Cons[u1,u]==free:
            nj=nj+1
            if u1<2.5:
                eq[nj-1]=-CP[u1,u]
            elif u1>2.5:
                eq[nj-1]=CP[u1,u]
            eqcoe[nj-1]={0}
            for u2 in range(0,n1):
                eq[nj-1]=eq[nj-1]+Oforce[rel[0,u2]-1][u1,3+rel[1,u2]]
                eqcoe[nj-1]=eqcoe[nj-1].union(oforcecoe[rel[0,u2]-1])
            eq[nj-1]=simplify(eq[nj-1])
        else:
            nj=nj+1
            eq[nj-1]=simplify(Oforce[rel[0,0]-1][u1,1+rel[1,0]]-Cons[u1,u]);
            eqcoe[nj-1]=oforcecoe[rel[0,0]-1]
print('Equations generated complete')
#vari=[];
coeffm=lil_matrix((cnumbers, cnumbers))
coeffm2=rand(cnumbers)
from giacpy import expand
from sympy import simplify
for u in range(0,cnumbers):
    t=0
    eq1=sympify(str(expand(eq[u])))
    for u1 in eqcoe[u]:
        t1=eq1.coeff(c[u1])
        if t1!=0:
            coeffm[u,u1]=t1
            t=t+t1*c[u1]
    eq1t=t-eq1
    coeffm2[u]=eq1t
    print(u," row complete")
print('begin to solve equations')
coeffm=coeffm.tocsr()
sol1=spsolve(coeffm,coeffm2)
print('done')
#print(sol)
print('Substituting...')
#Axialeqn=Axialeqn.subs(sol)
for u in range(0,ne):
    for u1 in range(0,2):
        t1=Axialcoe[2*u+u1]
        l1=len(t1)
        for u2 in range(0,l1):
            Axialeqn[u,u1]=Axialeqn[u,u1].subs(c[t1[u2]],sol1[t1[u2]])
print('Axialeqn=',Axialeqn)
#Lateraleqny=Lateraleqny.subs(sol)
for u in range(0,ne):
    for u1 in range(0,4):
        t1=Lateralycoe[4*u+u1]
        l1=len(t1)
        for u2 in range(0,l1):
            Lateraleqny[u,u1]=Lateraleqny[u,u1].subs(c[t1[u2]],sol1[t1[u2]])
print('Lateraleqny=',Lateraleqny)
#Lateraleqnz=Lateraleqnz.subs(sol)
for u in range(0,ne):
    for u1 in range(0,4):
        t1=Lateralzcoe[4*u+u1]
        l1=len(t1)
        for u2 in range(0,l1):
            Lateraleqnz[u,u1]=Lateraleqnz[u,u1].subs(c[t1[u2]],sol1[t1[u2]])
print('Lateraleqnz=',Lateraleqnz)
#Torqueeqn=Torqueeqn.subs(sol)
for u in range(0,ne):
    for u1 in range(0,2):
        t1=Torquecoe[2*u+u1]
        l1=len(t1)
        for u2 in range(0,l1):
            Torqueeqn[u,u1]=Torqueeqn[u,u1].subs(c[t1[u2]],sol1[t1[u2]])
print('Torqueeqn=',Torqueeqn)
print('Substitution complete')
#begin to write xls
print('Begin to write xls')
f = xlwt.Workbook()
sheet1 = f.add_sheet('Result',cell_overwrite_ok=True)
row1=['Dx','Dy','Dz','Rx','Ry','Rz','Fx','Fy','Fz','Mx','My','Mz','Position']
u1=0
for u in range(1,25):
    if u<7:
        sheet1.write(2,u,row1[u1],set_style('Times New Roman',220,True))
        sheet1.write(2,u+6,row1[u1],set_style('Times New Roman',220,True))
        u1=u1+1
    elif u>=13 and u<19:
        sheet1.write(2,u,row1[u1],set_style('Times New Roman',220,True))
        sheet1.write(2,u+6,row1[u1],set_style('Times New Roman',220,True))
        u1=u1+1
for u in range(25,37):
    if u%2==1:
        sheet1.write(2,u,row1[u//2-6],set_style('Times New Roman',220,True))
    elif u%2==0:
        sheet1.write(2,u,row1[12],set_style('Times New Roman',220,True))
for u in range(37,49):
    if u%2==1:
        sheet1.write(2,u,row1[u//2-12],set_style('Times New Roman',220,True))
    elif u%2==0:
        sheet1.write(2,u,row1[12],set_style('Times New Roman',220,True))
sheet1.write(1,1,'Former end',set_style('Times New Roman',220,True))
sheet1.write(1,7,'Latter end',set_style('Times New Roman',220,True))
sheet1.write(1,13,'Former end',set_style('Times New Roman',220,True))
sheet1.write(1,19,'Latter end',set_style('Times New Roman',220,True))
sheet1.write(0,1,'Displacements',set_style('Times New Roman',220,True))
sheet1.write(0,13,'Internal Forces',set_style('Times New Roman',220,True))
sheet1.write(0,25,'Maximum Forces',set_style('Times New Roman',220,True))
sheet1.write(0,37,'Minimum Forces',set_style('Times New Roman',220,True))
from sympy import *
for u in range(0,ne):
    u1=u+3
    sheet1.write(u1,0,u+1)
    sheet1.write(u1,1,float(Axialeqn[u,0].subs(x,0).evalf()))
    sheet1.write(u1,2,float(Lateraleqny[u,0].subs(x,0).evalf()))
    sheet1.write(u1,3,float(Lateraleqnz[u,0].subs(x,0).evalf()))
    sheet1.write(u1,4,float(Torqueeqn[u,0].subs(x,0).evalf()))
    sheet1.write(u1,5,float(Lateraleqnz[u,1].subs(x,0).evalf()))
    sheet1.write(u1,6,float(Lateraleqny[u,1].subs(x,0).evalf()))
    sheet1.write(u1,7,float(Axialeqn[u,0].subs(x,l[u,0]).evalf()))
    sheet1.write(u1,8,float(Lateraleqny[u,0].subs(x,l[u,0]).evalf()))
    sheet1.write(u1,9,float(Lateraleqnz[u,0].subs(x,l[u,0]).evalf()))
    sheet1.write(u1,10,float(Torqueeqn[u,0].subs(x,l[u,0]).evalf()))
    sheet1.write(u1,11,float(Lateraleqnz[u,1].subs(x,l[u,0]).evalf()))
    sheet1.write(u1,12,float(Lateraleqny[u,1].subs(x,l[u,0]).evalf()))
    sheet1.write(u1,13,float(Axialeqn[u,1].subs(x,0).evalf()))
    sheet1.write(u1,14,float(Lateraleqny[u,3].subs(x,0).evalf()))
    sheet1.write(u1,15,float(Lateraleqnz[u,3].subs(x,0).evalf()))
    sheet1.write(u1,16,float(Torqueeqn[u,1].subs(x,0).evalf()))
    sheet1.write(u1,17,float(Lateraleqnz[u,2].subs(x,0).evalf()))
    sheet1.write(u1,18,float(Lateraleqny[u,2].subs(x,0).evalf()))
    sheet1.write(u1,19,float(Axialeqn[u,1].subs(x,l[u,0]).evalf()))
    sheet1.write(u1,20,float(Lateraleqny[u,3].subs(x,l[u,0]).evalf()))
    sheet1.write(u1,21,float(Lateraleqnz[u,3].subs(x,l[u,0]).evalf()))
    sheet1.write(u1,22,float(Torqueeqn[u,1].subs(x,l[u,0]).evalf()))
    sheet1.write(u1,23,float(Lateraleqnz[u,2].subs(x,l[u,0]).evalf()))
    sheet1.write(u1,24,float(Lateraleqny[u,2].subs(x,l[u,0]).evalf()))
    a1=fMaxMin(Axialeqn[u,1],x,0,l[u,0])
    a2=fMaxMin(Lateraleqny[u,3],x,0,l[u,0])
    a3=fMaxMin(Lateraleqnz[u,3],x,0,l[u,0])
    a4=fMaxMin(Torqueeqn[u,1],x,0,l[u,0])
    a5=fMaxMin(Lateraleqnz[u,2],x,0,l[u,0])
    a6=fMaxMin(Lateraleqny[u,2],x,0,l[u,0])
    sheet1.write(u1,25,float(a1[0]))
    sheet1.write(u1,26,float(a1[1]))
    sheet1.write(u1,27,float(a2[0]))
    sheet1.write(u1,28,float(a2[1]))
    sheet1.write(u1,29,float(a3[0]))
    sheet1.write(u1,30,float(a3[1]))
    sheet1.write(u1,31,float(a4[0]))
    sheet1.write(u1,32,float(a4[1]))
    sheet1.write(u1,33,float(a5[0]))
    sheet1.write(u1,34,float(a5[1]))
    sheet1.write(u1,35,float(a6[0]))
    sheet1.write(u1,36,float(a6[1]))
    sheet1.write(u1,37,float(a1[2]))
    sheet1.write(u1,38,float(a1[3]))
    sheet1.write(u1,39,float(a2[2]))
    sheet1.write(u1,40,float(a2[3]))
    sheet1.write(u1,41,float(a3[2]))
    sheet1.write(u1,42,float(a3[3]))
    sheet1.write(u1,43,float(a4[2]))
    sheet1.write(u1,44,float(a4[3]))
    sheet1.write(u1,45,float(a5[2]))
    sheet1.write(u1,46,float(a5[3]))
    sheet1.write(u1,47,float(a6[2]))
    sheet1.write(u1,48,float(a6[3]))
    print(u,"th")
#for u in range(27,36):
    #for u1 in range(0,cnumbers+1):
        #sheet1.write(u,u1+1,float(coeffm[u,u1]),set_style('Times New Roman',220,True))
    #sheet1.write(u,38,str(eq[u]),set_style('Times New Roman',220,True))

f.save('D:\\PyProgram\\3DResult.xls')
