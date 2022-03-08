from tkinter import E
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
    return(round(math.degrees(math.acos(x)),5))
def atan(x):
    return(round(math.degrees(math.atan(x),5)))
def mg(vec):
    mag = 0
    for i in range(3):
        mag+=vec[i]**2
    return(mag**0.5)
def qd(a,b,c):
    E1 = (-b + (b**2-4*a*c)**0.5)/(2*a)
    E2 = (-b - (b**2-4*a*c)**0.5)/(2*a)
    return([E1,E2])
def dt(a,b):
    return(a[0]*b[0]+a[1]*b[1]+a[2]*b[2])
def vecSum(a,b):
    return(a[0]+b[0],a[1]+b[1],a[2]+b[2])
def vecSub(a,b):
    return(a[0]-b[0],a[1]-b[1],a[2]-b[2])
def vecScale(a,b):
    return([a[0]*b,a[1]*b,a[2]*b])
def calcP3(L,P2,P3Ops):
    P3Z = qd((2*P2[2]-2*L[4])**2+4*(P2[0]**2+P2[1]**2),
    4*(L[4]-P2[2])*(-L[2]**2+L[3]**2-L[4]**2+mg(P2)**2)-8*L[4]*(P2[0]**2+P2[1]**2),
    (-L[2]**2+L[3]**2-L[4]**2+mg(P2)**2)**2-4*(P2[0]**2+P2[1]**2)*(L[3]**2-L[4]**2))[P3Ops[0]]
    P3Y = [((L[3]**2-(P3Z-L[4])**2)/((P2[0]**2/P2[1]**2)+1))**0.5,-((L[3]**2-(P3Z-L[4])**2)/((P2[0]**2/P2[1]**2)+1))**0.5][P3Ops[1]]
    P3X = P3Y*P2[0]/P2[1]
    return([P3X,P3Y,P3Z])
a = 25
fig = plt.figure()
ax = Axes3D(fig)
ax.set_xlim3d(0, a+10)
ax.set_ylim3d(0, a+10)
ax.set_zlim3d(0, a+10)
ax.set_box_aspect([ub - lb for lb, ub in (getattr(ax, f'get_{a}lim')() for a in 'xyz')])

# Varing:
L = [5.5,6.25,22.25,22.25,6]
# L = [10.5,10.25,22.25,22.25,6]
TP = [15,5,25]
TRA = [0.5,135.5] # [longitude,latitude]
# Vectors:
O = [0,0,L[4]]
TRV = [cos(TRA[0])*cos(TRA[1]),sin(TRA[0])*cos(TRA[1]),sin(TRA[1])]
print(TRV[0])
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
P3Ops = [1,1] # <-- 0 for positive 1 for negative on quadratic
P4 = [0,0,L[4]]
P3s = [calcP3(L,P2,[0,0]),calcP3(L,P2,[0,1]),calcP3(L,P2,[1,0]),calcP3(L,P2,[1,1])]
P3t = []
Lprec= 4
i = 0
while i < 4:
    if round(mg(vecSub(P2,P3s[i])),Lprec) == L[2] and round(mg(vecSub(P4,P3s[i])),Lprec) == L[3]:
        if P3s[i][0] >= 0: #P3 Forward
            if P2[2] < (P2[0]*P3s[i][2]/P3s[i][0]+P4[2]):
                P3 = P3s[i]
        else: #P3 Back
            if P2[2] > (P2[0]*P3s[i][2]/P3s[i][0]+P4[2]):
                P3 = P3s[i]
    i += 1
# Angles:
angles = [acos((dt(vecScale(TRV,-1),vecSub(P2,P1)))/(mg(vecScale(TRV,-1))*mg(vecSub(P2,P1)))), #A1
    acos((dt(vecSub(P3,P2),vecSub(P1,P2)))/(mg(vecSub(P3,P2))*mg(vecSub(P1,P2)))), #A2
    acos((dt(vecSub(P4,P3),vecSub(P2,P3)))/(mg(vecSub(P4,P3))*mg(vecSub(P2,P3)))), #A3
    acos((dt(vecSub(P3,P4),[0,0,-1]))/(mg(vecSub(P3,P4)))), #A4
    acos(-P3[0]/mg([P3[0],P3[1],0])) #A5
]
print("origin " + str(angles[4]))
#need to change angles to add 180 or not(A1,A2,A4) (+-90 on A5)
if dt([P1[0],P1[1],0],[1,0,0])>0: #P1 forwards
    if dt(vecScale(TRV,-1),[-P1[1]/P1[0],1,0])>0:
        #End clockwise
        angles[0] = 360 - angles[0]
else: #P1
    if dt(vecScale(TRV,-1),[-P1[1]/P1[0],1,0])<0:
        #End clockwise
        angles[0] += 180
if P3[0] < 0 :
    angles[3] = 360-angles[3]
    if P3[1] < 0:
        angles[4] = acos(P3[0]/mg([P3[0],P3[1],0]))
    else:
        angles[4] = 360 - acos(P3[0]/mg([P3[0],P3[1],0]))
    print("Trigger " + str(angles[4]))
else:
    if P3[1] < 0:
        angles[4] = 360 - angles[4]
if P2[0]-P3[0] > 0:
    if P1[2] > P2[2]+(P1[0]-P2[0])*(P2[2]-P3[2])/(P2[0]-P3[0]):
        angles[1] = 360-angles[1]
else:
    if P1[2] < P2[2]+(P1[0]-P2[0])*(P2[2]-P3[2])/(P2[0]-P3[0]):
        angles[1] = 360-angles[1]
print(P3)
print(angles)
print(mg(vecSub(P2,P3)))
print(mg(vecSub(P4,P3)))
# Plotting:
plt.plot([TP[0]+2,TP[0],TP[0],TP[0],TP[0]],[TP[1],TP[1],TP[1]+2,TP[1],TP[1]],[TP[2],TP[2],TP[2],TP[2],TP[2]+2],'purple')
plt.plot([TP[0],P1[0],P2[0]],[TP[1],P1[1],P2[1]],[TP[2],P1[2],P2[2]],'green')
plt.plot([P1[0],10*N[0]/mg(N)+P1[0]],[P1[1],10*N[1]/mg(N)+P1[1]],[P1[2],10*N[2]/mg(N)+P1[2]],'blue')
plt.plot([P2[0],P3[0],P4[0]],[P2[1],P3[1],P4[1]],[P2[2],P3[2],P4[2]],'orange')
plt.plot([P4[0],0],[P4[1],0],[P4[2],0],'pink')
plt.plot([P2[0],P1[0]],[P2[1],P1[1]],[P2[2],P2[2]+(P1[0]-P2[0])*(P2[2]-P3[2])/(P2[0]-P3[0])],'red')
ax.plot3D([0,-a,-a,-a,a,a],[0,0,-a,a,a,a],[0,0,0,0,0,2*a],'gray')
plt.draw()
plt.show()
