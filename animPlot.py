from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import math
plt.style.use('seaborn-pastel')
fig = plt.figure()
ax = plt.axes(projection='3d')
# plt.axis('equal')

# jointLocations = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]] 
# jl = jointLocations
# x = [jl[0][0],jl[1][0],jl[2][0],jl[3][0],jl[4][0]]
# y = [jl[0][1],jl[1][1],jl[2][1],jl[3][1],jl[4][1]]
# z = [jl[0][2],jl[1][2],jl[2][2],jl[3][2],jl[4][2]]
# plt.plot(x,y,z)
# L0 = 5
# L1 = 5
R0 = 0.5
R1 = 0.5
TR = [150,200]
TL = [3,3,5]
AL = [7,7,1,1]
i = 0
def calcLocLocs (target,L0,L1):
    lenP = (target[0]**2+target[2]**2)**0.5
    lenH = (lenP**2+target[1]**2)**0.5
    if target[2] > 0:
        angN0a = math.degrees(math.asin(target[2]/lenP))
    else:
        angN0a = -math.degrees(math.asin(target[2]/lenP))
    angN0 = 180 + angN0a
    angN1 = 180 +  math.degrees(math.acos((L0**2+lenH**2-L1**2)/(2*L0*lenH))) + math.degrees(math.asin(target[1]/lenH))
    angN2 = math.degrees(math.acos((L0**2+L1**2-lenH**2)/(2*L0*L1)))
    angN3aa = 180 - math.degrees(math.acos((L0**2+lenH**2-L1**2)/(2*L0*lenH))) - angN2
    angN3ab = math.degrees(math.asin(lenP/lenH))
    angN3a = angN3aa + angN3ab
    angN3 = angN3a+90
    lenN2xa = math.cos(math.radians(angN1-180))*L0
    pointN2 = [math.cos(math.radians(angN0-180))*lenN2xa,math.sin(math.radians(angN1-180))*L0,math.sin(math.radians(angN0-180))*lenN2xa]
    
    plotPoints = [[0,0,0],pointN2,target]
    return([[angN0,angN1,angN2,angN3],plotPoints])

def calcRotLocs(target,TRots,N3l,N4l):
    pointN4 = [0,0,0]
    deltaN4y = math.cos(math.radians(270-TRots[0]))*N4l
    N4p = math.sin(math.radians(270-TRots[0]))*N4l
    deltaN4x = math.sin(math.radians(270-TRots[1]))*N4p
    deltaN4z = math.cos(math.radians(270-TRots[1]))*N4p
    #z
    if TRots[1] < 180:
        pointN4[2] = target[2]+deltaN4z
    else:
        pointN4[2] = target[2]-deltaN4z
    #y
    if TRots[0] <180:
        pointN4[1] = target[1]+deltaN4y
    else:
        pointN4[1] = target[1]-deltaN4y
    #x
    if TRots[1]<90 or TRots[1]>270:
        pointN4[0] = target[0]+deltaN4x
    else:
        pointN4[0] = target[0]-deltaN4x
    vectorP = [0,1,0]
    vectorP[2] = ((pointN4[0]*pointN4[2]*vectorP[1]*(pointN4[1]-target[1]))/(pointN4[0]*pointN4[0]*(target[0]-pointN4[0])+pointN4[0]*pointN4[2]*(target[2]-pointN4[2])))
    vectorP[0] = ((pointN4[0]*vectorP[1]*(pointN4[1]-target[1]))/(pointN4[0]*(target[0]-pointN4[0])+pointN4[2]*(target[2]-pointN4[2])))
    pointP = [pointN4[0]-vectorP[0],pointN4[1]-vectorP[1],pointN4[2]-vectorP[2]]
    vecNT = [target[0]-pointN4[0],target[1]-pointN4[1],target[2]-pointN4[2]]
    vecNP = [pointP[0]-pointN4[0],pointP[1]-pointN4[1],pointP[2]-pointN4[2]]
    print("dot product: (3dp)\n" + str(round(vecNT[0]*vecNP[0] + vecNT[1]*vecNP[1]+vecNT[2]*vecNP[2],3)))
    vectorN3 = [0,1,0]
    print
    vectorN3[0] = ((-pointP[0]*vectorN3[1]*(pointP[1]-pointN4[1]))/(pointP[0]*(pointP[0]-pointN4[0])+pointP[2]*(pointP[2]-pointN4[2])))
    vectorN3[2] = ((-pointP[2]*vectorN3[1]*(pointP[1]-pointN4[1]))/(pointP[0]*(pointP[0]-pointN4[0])+pointP[2]*(pointP[2]-pointN4[2])))
    vecNP = [pointP[0]-pointN4[0],pointP[1]-pointN4[1],pointP[2]-pointN4[2]]
    constantN3 = ((N3l**2)/(vectorN3[0]**2+vectorN3[1]**2+vectorN3[2]**2))**0.5
    scaledVectorN3 = [vectorN3[0]*constantN3,vectorN3[1]*constantN3,vectorN3[2]*constantN3]
    pointN3 = [pointN4[0]-scaledVectorN3[0],pointN4[1]-scaledVectorN3[1],pointN4[2]-scaledVectorN3[2]]
    print("dot product: (3dp)\n" + str(round(scaledVectorN3[0]*vecNP[0] + scaledVectorN3[1]*vecNP[1]+scaledVectorN3[2]*vecNP[2],3)))
    return([pointN3,pointN4,pointP])
def getAngles(TL,TR,AL):
    rotDat = calcRotLocs(TL,TR,AL[2],AL[3])
    locDat = calcLocLocs(rotDat[0],AL[0],AL[1])
    if rotDat[1][1] > rotDat[0][1]:
        ang3b = math.degrees(math.asin((rotDat[1][1]-rotDat[0][1])/TL[2]))
    else:
        ang3b = -math.degrees(math.asin((rotDat[1][1]-rotDat[0][1])/TL[2]))
    ang3 = locDat[0][3]+ ang3b
    magSquaredLT = (rotDat[0][0]-TL[0])**2+(rotDat[0][1]-TL[1])**2+(rotDat[0][2]-TL[2])**2
    ang4 = math.degrees(math.acos((AL[2]**2+AL[3]**2-magSquaredLT)/(2*AL[2]*AL[3])))
    print("Angles(3dp):\n" + str(round(locDat[0][0],3)),str(round(locDat[0][1],3)),str(round(locDat[0][2],3)),str(round(ang3,3)),str(round(ang4,3)))
    return(locDat[0][0],locDat[0][1],locDat[0][2],ang3,ang4)
def getPoints(TL,TR,AL):
    rotDat = calcRotLocs(TL,TR,AL[2],AL[3])
    locDat = calcLocLocs(rotDat[0],AL[0],AL[1])
    if rotDat[1][1] > rotDat[0][1]:
        print((rotDat[1][1]-rotDat[0][1])/TL[2])
        ang3b = math.degrees(math.asin((rotDat[1][1]-rotDat[0][1])/TL[2]))
    else:
        ang3b = -math.degrees(math.asin((rotDat[1][1]-rotDat[0][1])/TL[2]))
    ang3 = locDat[0][3]+ ang3b
    magSquaredLT = (rotDat[0][0]-TL[0])**2+(rotDat[0][1]-TL[1])**2+(rotDat[0][2]-TL[2])**2
    ang4 = math.degrees(math.acos((AL[2]**2+AL[3]**2-magSquaredLT)/(2*AL[2]*AL[3])))
    print("Angles(3dp):\n" + str(round(locDat[0][0],3)),str(round(locDat[0][1],3)),str(round(locDat[0][2],3)),str(round(ang3,3)),str(round(ang4,3)))
    # ax.plot3D([rotDat[2][0],rotDat[1][0],TL[0]],[rotDat[2][2],rotDat[1][2],TL[2]], [rotDat[2][1],rotDat[1][1],TL[1]], 'blue')
    # ax.plot3D([rotDat[0][0],rotDat[1][0],TL[0]], [rotDat[0][2],rotDat[1][2],TL[2]], [rotDat[0][1],rotDat[1][1],TL[1]], 'red')
    # ax.plot3D([locDat[1][0][0],locDat[1][1][0],locDat[1][2][0]],[locDat[1][0][2],locDat[1][1][2],locDat[1][2][2]],[locDat[1][0][1],locDat[1][1][1],locDat[1][2][1]], 'purple')
    # plt.draw()
    # plt.show()
    return([[locDat[1][0],locDat[1][1],locDat[1][2],rotDat[1],TL],[locDat[0][0],locDat[0][1],locDat[0][2],ang3,ang4]])
def getPlots(TL,TR,AL):
    data = getPoints(TL,TR,AL)
    return([[data[0][0][0],data[0][1][0],data[0][2][0],data[0][3][0],data[0][4][0]],[data[0][0][1],data[0][1][1],data[0][2][1],data[0][3][1],data[0][4][1]],[data[0][0][2],data[0][1][2],data[0][2][2],data[0][3][2],data[0][4][2]]])
def plotPoints(a):
    if a != 0:
        ax.clear()
    print("a:")
    print(a)
    print("x:")
    # print(x)
    print('val:')
    print((a*6)+1)
    TR = [120,(a*6)+1]
    TL = [4,3,4]
    AL = [5,5,1,1]
    point = getPlots(TL,TR,AL)
    plt.plot(point[0][0:2],point[2][0:2],point[1][0:2],'purple')
    plt.plot(point[0][1:3],point[2][1:3],point[1][1:3],'green')
    plt.plot(point[0][2:4],point[2][2:4],point[1][2:4],'blue')
    plt.plot(point[0][3:5],point[2][3:5],point[1][3:5],'orange')
    # plt.plot(point[0],point[2],point[1],'blue')
    ax.plot3D([0,-20,-20,-20,40,40],[0,0,-20,40,40,40],[0,0,0,0,0,40],'gray')
    plt.draw()
    # plt.show()

# ani = FuncAnimation(fig, plotPoints,interval=16)
# plt.show()
TR = [181.00001,180.001]
TL = [22.5,22.5,0.1]
AL = [22.5,22.5,6.41,5.05]
point = getPlots(TL,TR,AL)
plt.plot(point[0][0:2],point[2][0:2],point[1][0:2],'purple')
plt.plot(point[0][1:3],point[2][1:3],point[1][1:3],'green')
plt.plot(point[0][2:4],point[2][2:4],point[1][2:4],'blue')
plt.plot(point[0][3:5],point[2][3:5],point[1][3:5],'orange')
# plt.plot(point[0],point[2],point[1],'blue')
ax.plot3D([0,-20,-20,-20,40,40],[0,0,-20,40,40,40],[0,0,0,0,0,40],'gray')
plt.draw()
plt.show()
#Note to reader: all above code is purely developmental. You should have simular expectations for it as you would for scribbled down notes.
