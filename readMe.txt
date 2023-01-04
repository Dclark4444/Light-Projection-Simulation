The program found within this file path simulates how light travels, including "bending" due to time dilation of objects with large mass, as well as fading in intensity as the light travels from its source.
The simulation requires an input json file of the requested scenario to simulate as well as how many light rays per source are requested to be simulated.

It should be noted that a writeup with pictures and charts for a better understanding of the project can be found in the file path this text file is found in.

Table of Content:
1. How the simulation works
2. The units of the input scenarios
3. Making an input json file
4. How to run the simulation

------------------------------
1. How the simulation works
The simulation first loads the specified json file and breaks up the three possible objects in to separate data structures.
Then, the angle needed to evenly simulate light rays from each source object is found by dividing 360 degrees by the number of requested light rays per source.
The program then loops through every light source, doing the following each time for each light ray:
- finds the angle of the light source by taking the previously found angle and multiplying it by the number of light rays simulated for that light source
- finds the starting coordinate pair for the current light ray by doing the following algorithm, (lightSourcesXCoordinate+lightSourceRadius*cos(currentRaysAngle), lightSourceYCoordinate+lightSourceRadius*sin(currentRaysAngle))
- The ray's angle is changed if any planets are within range using the following equations, sin(angleBetweenLightRayAndMass-currentAngle))*(angleChangeDueToGravity), angleChangeDueToGravity = ((gravitationalConstant*planetMass)/(distanceBetween(rayCoordinate, planetCoordinate)*(speedOfLight**2)))*4
- The current rays coordinates is moved using the following equation, (currentRayXCoordinate+cos(currentRaysAngle), currentRayYCoordinate+sin(currentRaysAngle)), then distance is increased by 1 km, and the intensity of the light is diminished proportionally using the inverse square law, currentRaysLumen = currentRaysLumen/(4*pi*(distance**2))
- The previous two steps are repeated until the light is collected, runs into a planet or source, or fades below 1 Lumen
- The collected intensities for each collection point is then averaged by the number of rays that made it to the collection point

1. A. A short example simulation

Input scenario (This is testInput1.json):
A light source at (100km, 100km), radius of 10 km, and intensity of 100000 Lumen
A collection point at (150km, 100km) and radius of 5km
Simulation 4 light rays per source

If the user wanted to simulate 4 light rays, a very small number, the simulation would do 360 degrees/4 which equals 90 degrees between each light ray revolving around the light source.
Then the simulation would start simulating light rays.
For light ray 1:
angle = 90*0=0 degrees
starting coordinatinates = (100km+10km*cos(0), 100km+10km*sin(0)) = (110km, 100km) #This is the surface of the light source
Then the light begins to travel,
There are no planets nearby, and the source has a very small mass so its negligible, to change the light ray's direction, so angle = 0 degrees
new coordinates = (110+cos(0), 100+sin(0)) = (111km, 100km)
Distance is now equal to 1km, the light rays intensity changes by 100000/(4*pi*(1**2)) = 7957.747 Lumen
This repeats until the light ray eventually reaches the collection point with 6.140 Lumen left

The other light rays have angles of 90, 180, and 270 degrees, all of which would just go off into space and dissipate.
Since only one light ray made it to the collection polint, 6.140Lumen/1 = 6.140 Lumen as a final output

------------------------------
2. The units of the input scenarios

All radi, distances, and coordinates are in kilometers. (0, 0) is the origin in all coordinate systems
Intensity of light is measured in Lumen.
Mass is in kilograms.

It should be noted collection points do not have a mass, and will not cause light to bend due to time dilation. If this effect is desired, add a planet with a radius just smaller than the collection point with the same location

------------------------------
3. Making an input json file

The input will need the object's name as a key and a list of the following: object type, pixel location, radius, luminosity (if applicable), and mass (if applicable).

The following objects need the following input:
-Planets: ["planet", pixel location, radius, mass]
-Sources: ["source", pixel location, radius, light intensity, mass]
-Collections: ["collection", pixel location, radius]

Json files follow python dictionary format, objects are listed inside curly brackets {}, each item needs a key (a string in this instance) followed by a colon :, and then the object elements are listed in brackets []. All strings need to be quotes "" and all listed items need commas after them. Coordinates need to be in a list with brackets [].
Here us an example input json (testInput4.json):
{"Star": ["source", [100, 100], 10, 2000000, 1],
"Planet": ["planet", [150, 100], 10, 100000000000000000000000000],
"Collection": ["collection", [180, 100], 10]}

Note the entering down is not necessary to make a valid json.

------------------------------
4. How to run the simulation

You must have python 3 installed to run the simulation, python 3 can be found at python.org and download the most recent build for you operating system.
This program was built in python 3.10.6.

To run the simulation doubleclick on the file titled "simulation.py" found in the folder this readMe was found in. It should open a black terminal provide instruction from there.
You should see a menu where you input a number ranging from 1-3, with 1 being the option to run the simulation, type in "1" without the quotes and press enter.
It should instruct you to input the file name of the input json file you wish to simulate, "testInputJson4.json" without the quotes is a valid input, and then the program will ask for the number of rays you wish to simulate for each light source. This number must be an integer and more than 0, it recommended to have an integer no lower than 3600.

To set the simulation to output individual ray paths, a very computer intensive setting causing the simulation to increase in run time, enter the option 2 in the menu. For this option it is recommended to use less than 32 light rays per light source.

Any added input json files must be put into the file titled "input" which can be found in the file path this readMe was found.






