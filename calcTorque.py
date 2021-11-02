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
vals = calcTorque(22.5,22.5,6.41,5.05,0,0.01)
print("Torque (cm*Kg): " + str(vals[0]))
print("Reach (cm): " + str(vals[1]))