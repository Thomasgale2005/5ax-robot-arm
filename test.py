from turtle import bgcolor
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import math
def sin(x):
    return(round(math.sin(math.radians(x)),5))
def cos(x):
    return(round(math.cos(math.radians(x)),5))
def acos(x):
    return(round(math.degrees(math.acos(x),5)))
def atan(x):
    return(round(math.degrees(math.atan(x),5)))
def mg(vec):
    mag = 0
    for i in range(3):
        mag+=vec[i]**2
    return(mag**0.5)
def qd(a,b,c):
    print([a,b,c])
    E1 = (-b + (b**2-4*a*c)**0.5)/(2*a)
    E2 = (-b - (b**2-4*a*c)**0.5)/(2*a)
    return([E1,E2])
def dt(a,b):
    return(a[0]*b[0]+a[1]*b[1]+a[2]*b[2])
def vecSum(a,b):
    return(a[0]+b[0],a[1]+b[1],a[2]+b[2])
def vecSub(a,b):
    return(a[0]-b[0],a[1]-b[1],a[2]-b[2])
fig = plt.figure()
ax = Axes3D(fig)
ax.set_xlim3d(0, 150)
ax.set_ylim3d(0, 150)
ax.set_zlim3d(0, 150)
ax.set_box_aspect([ub - lb for lb, ub in (getattr(ax, f'get_{a}lim')() for a in 'xyz')])

# Varing:
# L = [5.5,6.25,22.25,22.25,6.25]
L = [10.5,10.25,22.25,22.25,6.25]
TP = [10,10,20]
TRA = [20,70]
# Vectors:
O = [0,0,L[4]]
TRV = [cos(TRA[0])*cos(TRA[1]),sin(TRA[0])*cos(TRA[1]),sin(TRA[1])]
P1 = [TRV[0]*L[0]/mg(TRV)+TP[0],TRV[1]*L[0]/mg(TRV)+TP[1],TRV[2]*L[0]/mg(TRV)+TP[2]]
OP1 = [P1[0]-O[0],
    P1[1]-O[1],
    P1[2]-O[2]]
N = [-TRV[2]*OP1[0]/(OP1[0]*TRV[0]+OP1[1]*TRV[1]),
    -TRV[2]/(OP1[0]*TRV[0]/OP1[1]+TRV[1]),
    1]
Q = [-N[2]*OP1[0]/(OP1[0]*N[0]+OP1[1]*N[1]),
    -N[2]/(OP1[0]*N[0]/OP1[1]+N[1]),
    1]
P2 = [Q[0]*L[1]/mg(Q)+P1[0],
    Q[1]*L[1]/mg(Q)+P1[1],
    Q[2]*L[1]/mg(Q)+P1[2]]
P3Ops = [0,0]
P3Z = qd((2*P2[2]-2*L[4])**2+4*(P2[0]**2+P2[1]**2),
    4*(L[4]-P2[2])*(-L[2]**2+L[3]**2-L[4]**2+mg(P2)**2)-8*L[4]*(P2[0]**2+P2[1]**2),
    (-L[2]**2+L[3]**2-L[4]**2+mg(P2)**2)**2-4*(P2[0]**2+P2[1]**2)*(L[3]**2-L[4]**2))[P3Ops[0]]
P3Y = [((L[3]**2-(P3Z-L[4])**2)/((P2[0]**2/P2[1]**2)+1))**0.5,-((L[3]**2-(P3Z-L[4])**2)/((P2[0]**2/P2[1]**2)+1))**0.5][P3Ops[1]]
P3 = [P3Y*P2[0]/P2[1],
    P3Y,
    P3Z]
P4 = [0,0,L[4]]
print([mg(vecSub(P2,P3)),mg(vecSub(P3,P4))], ([L[2],L[3]]))
print(P3)
# Angles:
angles = []
# Plotting:
plt.plot([TP[0]+2,TP[0],TP[0],TP[0],TP[0]],[TP[1],TP[1],TP[1]+2,TP[1],TP[1]],[TP[2],TP[2],TP[2],TP[2],TP[2]+2],'purple')
plt.plot([TP[0],P1[0],P2[0]],[TP[1],P1[1],P2[1]],[TP[2],P1[2],P2[2]],'green')
plt.plot([P1[0],10*N[0]/mg(N)+P1[0]],[P1[1],10*N[1]/mg(N)+P1[1]],[P1[2],10*N[2]/mg(N)+P1[2]],'blue')
plt.plot([P2[0],P3[0],O[0]],[P2[1],P3[1],O[1]],[P2[2],P3[2],O[2]],'orange')
plt.plot([O[0],0],[O[1],0],[O[2],0],'pink')
plt.plot([TP[0], TRV[0]+TP[0]],[TP[1], TRV[1]+TP[1]],[TP[2], TRV[2]+TP[2]],'blue')
ax.plot3D([0,-70,-70,-70,70,70],[0,0,-70,70,70,70],[0,0,0,0,0,140],'gray')
plt.draw()
plt.show()
