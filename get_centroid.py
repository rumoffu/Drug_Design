#!/usr/bin/env python
# Uses chimera to change to a directory,
# open all .pdb files
# defines the centroid and returns the coordinates of the centroid
# and add hydrogrens and then add charge using the ff99SB gasteiger method
# finishes by writing the output as a mol2 file
# run this with:
# chimera --nogui get_centroid.py
from os import chdir, listdir
from chimera import *

def save_reply_log(path):
  from chimera.tkgui import saveReplyLog
	saveReplyLog(r'~/vboxshared/research/sphere_gen/%s'  % path)
	print "saved to %s" % path
'''
   from chimera import dialogs
   r = dialogs.find('reply')
   print "found r:%s" % r
   text = r.text.get('1.0', 'end')
   f = open(path, 'w')
   f.write(text)
   f.close()
'''
chdir("receptors") # change to the receptors file directory
for pdb in listdir("."):
        if not pdb.endswith(".pdb"):
                continue
	# find centroid based on hydrophobicity
        runCommand("open " + pdb)
	runCommand("define centroid :/kdHydrophobicity=4.5")
	save_reply_log(pdb[:-4] + ".txt")
        runCommand("close all")

'''
	# addh and charge 
        runCommand("open " + pdb)
        runCommand("addh")
        runCommand("addcharge all chargeModel ff99SB method gas")
        runCommand("write format mol2 0 " + sdf[:-4] + "_charged.mol2")
        runCommand("close all")
'''

