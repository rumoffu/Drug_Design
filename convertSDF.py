#!/usr/bin/env python
# Uses chimera to change to a directory,
# open all .sdf files
# and add hydrogrens and then add charge using the ff99SB gasteiger method
# finishes by writing the output as a mol2 file
# run this with:
# chimera --nogui convertSDF.py
from os import chdir, listdir
from chimera import runCommand
chdir("odor_ligands") # change to the SDF file directory
for sdf in listdir("."):
        if not sdf.endswith(".sdf"):
                continue
        runCommand("open " + sdf)
        runCommand("addh")
        runCommand("addcharge all chargeModel ff99SB method gas")
        runCommand("write format mol2 0 " + sdf[:-4] + "_charged.mol2")
        runCommand("close all")
