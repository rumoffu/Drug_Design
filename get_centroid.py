#!/usr/bin/env python
# Uses chimera to
# open all .pdb files
# define the centroid and return the coordinates of the centroid
# run this with:
# chimera --nogui get_centroid.py
import sys
from os import chdir, listdir
from chimera import *
print "sys.argv[1] %s" % sys.argv[1]

runCommand("open " + sys.argv[1])
# find centroid based on hydrophobicity
runCommand("define centroid :/kdHydrophobicity=4.5")


