#!/usr/bin/env python
# takes all pdb files in the directory /receptors and prepares them for dock6

import os, subprocess
from subprocess import call
import sys 
from os import chdir, listdir 

#protonate 
root_path = '/damsl/projects/molecules/data/Odorant_GPCR/r_test'
cid = ""
if os.path.exists(os.path.join(root_path,cid)):
        directory_exists='true'
        os.chdir(os.path.join(root_path,cid))

	for pdb in listdir("."):
		if not pdb.endswith(".pdb"):
	                continue
	        if pdb.endswith("_mod2.pdb"):
			continue
		if pdb == "1gzm.pdb": #don't need to do the aligning pdb
			continue
	        cmd_st = ("python /damsl/projects/molecules/software/tools/pdb2pqr/pdb2pqr-1.8/pdb2pqr.py --ff=AMBER {0}.pdb {0}_mod2.pdb --ffout=AMBER --with-ph=7.0").format(pdb[:-4]) #protonate all pdb
	        print cmd_st
	        subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
	                shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	#root_path = '/damsl/projects/molecules/data/Odorant_GPCR'
#root_path = '/damsl/homes/kwong23/controlscripts'
#root_path = '/home/kwong23/controlscripts'

cid = ""
if os.path.exists(os.path.join(root_path,cid)):
	directory_exists='true'
	os.chdir(os.path.join(root_path,cid))

	#print(listdir("."))	
	cmd_st = ("chimera --nogui --silent align_all.py") #aligns all pdb
	#cmd_st = ("chimera --nogui align_all.py") #aligns all pdb
	print cmd_st #can add --silent above #this is for running from qp2 connected to /damsl/homes/kwong23
	subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
		shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()



#chdir("receptors") # change to the receptors file directory 
for pdb in listdir("."): 
        if not pdb.endswith("_aligned.pdb"): 
                continue 
        ###if pdb == "1gzm.pdb": # don't need to do the pdb used for align 
                ###continue 

	cmd_st = ('chimera --nogui --script "get_centroid.py {0}" > com.txt').format(pdb)
	print cmd_st
	subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
		shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	cmd_st = ('chimera --nogui --silent --script "place_helium.py {0}"').format(pdb)
	print cmd_st 
	subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
		shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	#root_path = '/damsl/homes/kwong23/controlscripts/receptors'
#	cid = "/receptors"
	cmd_st = ("chimera --nogui --silent {0}_noH.pdb writedms.py").format(pdb[:-4])
	print cmd_st
	subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
		shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	cmd_st = ("./sphgen_cpp")
	print cmd_st
	subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
		shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	cmd_st = ("./sphere_selector.exe rec.sph {0}.mol2 5").format(pdb[:-4])
	print cmd_st
	subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
		shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	cmd_st = ("mv selected_spheres.sph {0}.sph").format(pdb[:-12])
	print cmd_st
	subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
		shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	print "done with %s" % pdb
	#root_path = '/damsl/homes/kwong23/controlscripts'


