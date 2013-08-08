#!/usr/bin/env python
# takes all pdb files in the directory /receptors and prepares them for dock6

import os, subprocess
from subprocess import call
import sys 
from os import chdir, listdir 

#protonate 
root_path = '/damsl/projects/molecules/data/Odorant_GPCR/receptor_models/olfr1393/dock6_finegrid'
cid = ""
if os.path.exists(os.path.join(root_path,cid)):
        directory_exists='true'
        os.chdir(os.path.join(root_path,cid))

	for pdb in listdir("."):
		if not pdb.endswith(".pdb"):
	                continue
	        if "_mod2" in pdb: #do not do pdb2pqr again 
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

	cmd_st = ("rm OUTSPH")
	print cmd_st
	subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
		shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	cmd_st = ("sphgen -i INSPH -o OUTSPH")
	print cmd_st
	subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
		shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	cmd_st = ("sphere_selector rec.sph {0}.mol2 3").format(pdb[:-4])
	print cmd_st
	subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
		shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	cmd_st = ("rm rec.sph")
	print cmd_st
	subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
		shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	cmd_st = ("mv selected_spheres.sph {0}.sph").format(pdb[:-4])
	print cmd_st
	subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
		shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	showbox_file = open('showbox.in', 'w')
	showbox_file.write('Y\n8\n')
	message = '{0}.sph\n'.format(pdb[:-4])
	showbox_file.write(message)
	showbox_file.write('1\n')
	message = '{0}_box.pdb\n'.format(pdb[:-4])
	showbox_file.write(message)
	showbox_file.close()

        cmd_st = ("showbox < showbox.in")
        print cmd_st
        subprocess.Popen(cmd_st, cwd = os.path.join(root_path,cid),
                shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE).stdout.read()

	with open('grid.in', 'r') as file:
		# read a list of lines into data
		gridin = file.readlines()

	gridin[13] = 'receptor_file                  {0}_charged.mol2\n'.format(pdb[:-4])
	gridin[14] = 'box_file                       {0}_box.pdb\n'.format(pdb[:-4])
	gridin[16] = 'score_grid_prefix              {0}.grid'.format(pdb[:-4])


	# and write everything back
	with open('grid.in', 'w') as file:
	    file.writelines( gridin )
	print "done with %s" % pdb
	#root_path = '/damsl/homes/kwong23/controlscripts'

