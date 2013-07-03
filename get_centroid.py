#!/usr/bin/env python
# Uses chimera to change to a directory,
# open all .pdb files
# defines the centroid and returns the coordinates of the centroid
# and add hydrogrens and then add charge using the ff99SB gasteiger method
# finishes by writing the output as a mol2 file
# run this with:
# chimera --nogui get_centroid.py
import sys
from os import chdir, listdir
from chimera import *
print "sys.argv[3] %s" % sys.argv[3]

chdir("receptors")
print "done chdir receptors"
runCommand("open " + sys.argv[3])
# find centroid based on hydrophobicity
runCommand("define centroid :/kdHydrophobicity=4.5")
print "done get_centroid.py"
'''
        from DockPrep import prep
        models = chimera.openModels.list(modelTypes=[chimera.Molecule])
        prep(models)
        from WriteMol2 import writeMol2
        writeMol2(models, pdb[:-4]+ "_charged.mol2")
'''
'''
        # addh and charge 
        runCommand("addh")
        runCommand("addcharge all chargeModel ff99SB method gas")
        runCommand("write format mol2 0 " + pdb[:-4] + "_charged.mol2")
        runCommand("close all")
'''
