import json, math, os

def simulateLightRay (sourceCoord, sourceRadius, sourceLumens, angle, dictOfCollectionPoints, planets, rayNumber, showIndividualRays):
    returnValue = {}

    startPoint = [sourceCoord[0]+sourceRadius*math.cos(math.radians(angle)), sourceCoord[1]+sourceRadius*math.sin(math.radians(angle))]
    sourceLumens = sourceLumens
    currentRay = [startPoint, sourceLumens]
    distance = 0

    while currentRay[1] > 1:
        #Change the angle due to time dilation
        for x in planets:
            angle = lightBending(currentRay[0], x[0], x[2], angle)


        #Move a pixel over in the defined angle direction
        #Find change due to gravity of planets and add it here
        currentRay[0] = [currentRay[0][0]+math.cos(math.radians(angle)), currentRay[0][1]+math.sin(math.radians(angle))]
        distance+= 1
        #Reduce luminosity, r is the distance the ray has traveled in total
        currentRay[1] = sourceLumens/(4*math.pi*(distance**2))

        if showIndividualRays:
            print("Ray " + str(rayNumber) + ": " + str(currentRay[0][0]) + ", " + str(currentRay[0][0]))

        #Find end scenarios
        for x in dictOfCollectionPoints.keys():
            if math.dist(currentRay[0], dictOfCollectionPoints[x][0]) < dictOfCollectionPoints[x][1]:
                try:
                    returnValue[x] = returnValue[x] + currentRay[1]
                except:
                    returnValue[x] = currentRay[1]
                currentRay[1] = 0

        for x in planets:
            if math.dist(currentRay[0], x[0]) <= x[1]:
                currentRay[1] = 0


    return returnValue

def simulateLightSource (sourceCoord, sourceRadius, sourceLumens, dictOfCollectionPoints, raysPerSource, planets, sourceName, showIndividualRays):
    if showIndividualRays:
        print("For source named " + sourceName)
    collections = {}
    collectedRays = {}

    for x in range(raysPerSource):
        angle = (360/raysPerSource)*x
        returnValue = simulateLightRay(sourceCoord, sourceRadius, sourceLumens, angle, dictOfCollectionPoints, planets, x+1, showIndividualRays)

        if returnValue != {}:
            for y in returnValue.keys():
                try:
                    collections[y] = collections[y] + returnValue[y]
                except:
                    collections[y] = returnValue[y]
                try:
                    collectedRays[y] = collectedRays[y] + 1
                except:
                    collectedRays[y] = 1
    for x in collections.keys():
        collections[x] = collections[x]/collectedRays[x]
    return collections

def lightBending(rayCoordinate, planetCoordinate, planetMass, startAngle):
    gravitationalConstant = (6.6743*10**(-11))
    speedOfLight = 299792458
    angleChangeDueToGravity = math.degrees(((gravitationalConstant*planetMass)/(math.dist(rayCoordinate, planetCoordinate)*(speedOfLight**2)))*4)
    
    point1 = planetCoordinate
    point2 = rayCoordinate

    angleBetweenRayAndMass = math.atan2(point1[1] - point2[1], point1[0] - point2[0])

    if angleBetweenRayAndMass < 0:
        angleBetweenRayAndMass += math.radians(360)

    tempAngle = math.degrees(math.sin(angleBetweenRayAndMass - math.radians(startAngle)) * math.radians(angleChangeDueToGravity))

    if abs(tempAngle) > 0.00000000001:
        angle = startAngle + tempAngle
        if angle > 360:
            angle = angle - (angle // 360)*360
        elif angle < 0 and abs(angle) > 360:
            angle = angle + abs((angle//360))*360
    else:
        angle = startAngle
    return angle

def displayOutput(inputDict):
    returnString = ""
    if inputDict != {}:
        for x in inputDict.keys():
            returnString += 'The collection point titled "' + x + '" collected an average of ' + str(inputDict[x]) + " Lumen" + "\n"
    else:
        returnString = "There were no measurable light rays at the input collection points for this simulation"
    return returnString

def runSimulation(showIndividualRays):
    inputFileName = input("Please input the exact file name of the json file you wish to simulate:  ")
    if inputFileName[-5:] != ".json":
        inputFileName += ".json"
    print("If you are running the simulation without outputing individual ray coordinates it is reccomended to have no less than 3600 rays per light source. If you are running the simulation with outputing individual ray coordinates it is reccomended to have no more than 360 rays per light source.")
    inputRaysPerSource = int(input("Please input the number of rays you wish to simulate for each light source: "))

    print("Simulation is running...")

    with open(inputFileName, "r") as FILE:
        objects = json.load(FILE)

    #Break objects into individual lists
    dictOfCollectionPoints = {}
    sources = []
    planets = []

    for x in objects.keys():
        currentObject = objects[x]

        if currentObject[0] == "collection":
            dictOfCollectionPoints[x] = (currentObject[1], currentObject[2])
        if currentObject[0] == "planet":
            planets.append((currentObject[1], currentObject[2], currentObject[3]))
        if currentObject[0] == "source":
            planets.append((currentObject[1], currentObject[2], currentObject[4]))
            sources.append((currentObject[1], currentObject[2], currentObject[3], x))

    #Go through each source and simulate light
    globalCollections = {}
    for x in sources:
        collections = simulateLightSource(x[0], x[1], x[2], dictOfCollectionPoints, inputRaysPerSource, planets, x[3], showIndividualRays)
        for y in collections.keys():
            try:
                globalCollections[y] = globalCollections[y] + collections[y]
            except:
                globalCollections[y] = collections[y]

    print("Simulation has completed")

    print(displayOutput(globalCollections))

    input("Press enter to go back to the menu ")

#The start menu

showIndividualRays = False
runProgram = True
os.chdir("input")

print("""This program simulates how light travels, including the "bending" of light due to time dilation of objects with large mass, as well as fading in intensity as the light travels from its source.""")

while runProgram:
    if showIndividualRays:
        programString = "set to true"
    else:
        programString = "set to false"

    print("""To begin using this program, please enter one of the following commands:
1 - Run a simulation
2 - Switch the simulation to or not to display individual light paths (""" + programString + """)
3 - Exit the program""")
    print("Please input a command")
    try:
        userInput = int(input())
        if userInput == 1:
            runSimulation(showIndividualRays)
        elif userInput == 2:
            if showIndividualRays:
                showIndividualRays = False
            else:
                showIndividualRays = True
        elif userInput == 3:
            runProgram = False
        else:
            print("Sorry, that was an illegal command, please try again. Only numbers 1, 2, or 3 are permitted with no other characters.")
    except():
        print("Sorry, that was an illegal command, please try again. Only numbers 1, 2, or 3 are permitted with no other characters.")

