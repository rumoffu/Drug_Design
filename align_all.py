#!/usr/bin/env python
# Uses chimera to change to a directory,
# open all .pdb files
# align to 1gzm.pdb and write relative
# run this with:
# chimera --nogui align_all.py
import chimera
from os import chdir, listdir
from chimera import *

#chdir("receptors") # change to the receptors file directory
for pdb in listdir("."):
        if pdb.endswith("_aligned.pdb"):
		continue
	if pdb.endswith("_noH.pdb"):
		continue
        if not pdb.endswith("_mod2.pdb"): #originally was .pdb before pdb2pqr.py
                continue
	#if pdb == "1gzm.pdb": # don't need to do the pdb used for align
	#	continue
	runCommand("open " + pdb)
	runCommand("open 1gzm.pdb")
	runCommand("mmaker #1 #0")
	runCommand("write relative #1 #0 " + pdb[:-4] + "_aligned.pdb")
        runCommand("close all")
	pdb = pdb[:-4] + "_aligned.pdb"

	runCommand("open " + pdb)
	from DockPrep import prep
	models = chimera.openModels.list(modelTypes=[chimera.Molecule])
	prep(models)
	from WriteMol2 import writeMol2
	writeMol2(models, pdb[:-4]+ "_charged.mol2")

        runCommand("select H")
        runCommand("del sel")
        runCommand("write format pdb 0 " + pdb[:-4] + "_noH.pdb")
        runCommand("close all")


