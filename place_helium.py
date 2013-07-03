#!/usr/bin/env python
# 1) open text file and extract x y z from get_centroid.py output, com.txt
# 2) open $.pdb and place helium atom at that center
# 3) save $.pdb as $.mol2
# run this with:
# chimera --nogui place_helium.py

from chimera import selection
from chimera import Point
import BuildStructure
from chimera import runCommand
from chimera import openModels, Molecule
from os import chdir, listdir
import chimera
from WriteMol2 import writeMol2
import sys

        
file = open("com.txt")
for line in file:
	if line.find("centroid has center") != -1:
		#print "OPENED:%s" % line
		word = line.split()
		#print word
		x = float(word[3])
		y = float(word[4])
		z = float(word[5]) + 16
center = Point(x, y, z)
runCommand("open " + sys.argv[1])
model0 = openModels.list(id=0, modelTypes=[Molecule])[0]
c = BuildStructure.placeHelium('com', model=model0, position=center)
runCommand("select He")
runCommand("namesel helium")
runCommand("select helium za>10")
runCommand("del sel")
runCommand("del helium")
writeMol2(chimera.openModels.list(modelTypes=[chimera.Molecule]), sys.argv[1][:-4] + ".mol2")
runCommand("close all")


