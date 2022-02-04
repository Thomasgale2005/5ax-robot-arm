from pyfirmata import Arduino, SERVO
import time
import math
# port = '/dev/cu.usbmodem1101'
# pin = 10
# board = Arduino(port)
# board.digital[13].mode = SERVO
# def rotateServo(pin, angle):
#     print(angle)
#     board.digital[pin].write(((256*(angle-45))/360))
#     time.sleep(0.015)
def calcTorque(l1,l2,l3,l4,headMass,payloadMass):
    headMass = 0.0
    precision = 10
    total = 0
    # point 1
    i = 0
    while i < int(l1*precision):
        total += (0.075/(l1*precision))*((i/(l1*precision)))
        i+=1
    total += (l1)*0.1
    print(str(l1), str(total)) 
    # point 2
    i = 0
    while i < int(l2*precision):
        total += (0.075/(l2*precision))*((i/(l2*precision))+l1)
        i+=1
    total += (l1+l2)*0.1
    print(str(l2), str(total))
    # point 3:
    total += (l1+l2+l3)*0.1
    print(str(l3), str(total))
    # point 4
    total += (headMass+payloadMass)*(l4+l3+l2+l1)
    print(str(l4), str(total))
    return([total,l1+l2+l3+l4])

def calcLocLocs (target,L0,L1):
    lenP = (target[0]**2+target[2]**2)**0.5
    lenH = (lenP**2+target[1]**2)**0.5
    if target[2] > 0: 
        angN0a = math.degrees(math.asin(target[2]/lenP))
    else:
        angN0a = -math.degrees(math.asin(target[2]/lenP))
    angN0 = 180 + angN0a
    angN1 = math.degrees(math.acos((L0**2+lenH**2-L1**2)/(2*L0*lenH))) + math.degrees(math.asin(target[1]/lenH))
    angN2 = math.degrees(math.acos((L0**2+L1**2-lenH**2)/(2*L0*L1)))
    angN3aa = 180 - math.degrees(math.acos((L0**2+lenH**2-L1**2)/(2*L0*lenH))) - angN2
    angN3ab = math.degrees(math.asin(lenP/lenH))
    angN3a = angN3aa + angN3ab
    angN3 = angN3a+90
    lenN2xa = math.cos(math.radians(angN1))*L0
    pointN2 = [math.cos(math.radians(angN0-180))*lenN2xa,math.sin(math.radians(angN1))*L0,math.sin(math.radians(angN0-180))*lenN2xa]
    
    plotPoints = [[0,0,0],pointN2,target]
    return([[angN0,angN1+180,angN2,angN3],plotPoints])

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
    if (pointP[0]*(pointP[0]-pointN4[0])+pointP[2]*(pointP[2]-pointN4[2])) == 0:
        print("n30 == 0")
        print("n32 == 0")
        vectorN3[0] = (-pointP[0]*vectorN3[1]*(pointP[1]-pointN4[1]))/0.001
        vectorN3[2] = ((-pointP[2]*vectorN3[1]*(pointP[1]-pointN4[1]))/0.001)
    else:
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
    if TL[2] == 0:
        ang3b = 0
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
        ang3b = math.degrees(math.asin((rotDat[1][1]-rotDat[0][1])/TL[2]))
    else:
        ang3b = -math.degrees(math.asin((rotDat[1][1]-rotDat[0][1])/TL[2]))
    ang3 = locDat[0][3]+ ang3b
    magSquaredLT = (rotDat[0][0]-TL[0])**2+(rotDat[0][1]-TL[1])**2+(rotDat[0][2]-TL[2])**2
    ang4 = math.degrees(math.acos((AL[2]**2+AL[3]**2-magSquaredLT)/(2*AL[2]*AL[3])))
    print("Angles(3dp):\n" + str(round(locDat[0][0],3)),str(round(locDat[0][1],3)),str(round(locDat[0][2],3)),str(round(ang3,3)),str(round(ang4,3)))
    return([[locDat[1][0],locDat[1][1],locDat[1][2],rotDat[1],TL],[locDat[0][0],locDat[0][1],locDat[0][2],ang3,ang4]])
def moveRobot(targetLocations, targetRotations, armLengths, headMass, payloadMass):
    servoAngles = getAngles(targetLocations, targetRotations, armLengths)
    jointLocations = getPoints(targetLocations, targetRotations, armLengths)
    print(servoAngles)
    print(jointLocations)
TL = [22,22,5]
TR = [0,0]
AL = [22.5,22.5,6.41,1]
headMass = 0
payloadMass = 0.2
moveRobot(TL, TR, AL, headMass, payloadMass)
vals = calcTorque(22.5,22.5,6.41,5.05,0,0.01)
print(vals)