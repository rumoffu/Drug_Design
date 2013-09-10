import os, os.path, subprocess, tempfile
import glob
import datetime, time
from optparse import OptionParser
import sys
import base64
import xml.etree.ElementTree as ET
import cStringIO
import socket
import traceback
from threading import Thread
import re
import math
import random

def get_dock6_score():
        # score_dir = '/damsl/projects/molecules/data/Odorant_GPCR/receptor_models/olfr1393/dock6_grid_gpcrm_modeller_model8/bilayer_frames/gpcrm_modeller_model8_frame_466'
        # enter the directory
        # os.chdir(score_dir)
        # for ls *dock6*out
	for out in os.listdir('.'):
		if 'dock6' in out and out.endswith('.out'):
        #for out in os.listdir('*dock6*out'):
			print 'working on: ' + receptor + ' ' + frame + ' ' + out
			if 'no' in out:
				outfile = open('/damsl/projects/molecules/data/Odorant_GPCR/' + receptor + '_' + frame + '_no_scores.txt', 'w')
			else:
				outfile = open('/damsl/projects/molecules/data/Odorant_GPCR/' + receptor + '_' + frame + 'scores.txt', 'w')
			infile = open(out, 'r')
			lines = infile.readlines()
			for line in lines:
				if 'Molecule:' in line:
					molecule_name = line[10:].strip()
        	                if 'Grid Score:' in line:
					grid_score = line[25:].strip()
        	                        outfile.write(grid_score + '\t' + molecule_name + '\n')
                	                #print grid_score, molecule_name # score
                
os.chdir('/damsl/projects/molecules/data/Odorant_GPCR/receptor_models/olfr1393')
for receptor in os.listdir('.'):
	if 'dock6_grid_' in receptor:
	#for receptor in os.listdir('dock6_grid_*'):
        	os.chdir(receptor + '/bilayer_frames')
        	for frame in os.listdir('.'):
			if frame.endswith('.pdb'): continue
        	        os.chdir(frame)
        	        get_dock6_score()
        	        os.chdir('..') #exit frame folder
        	os.chdir('../..') #exit bilayer frames and receptor



'''
scores_list  = [line.strip() for line in open("/damsl/projects/molecules/data/Odorant_GPCR/receptor_models/olfr1393/oe_fred_high_gpcrm_model1/bilayer_frames/rosetta-modeller-model1_frame_45/list_odorator_scores", 'r')]
os.chdir('/damsl/projects/molecules/data/Odorant_GPCR/receptor_models/olfr1393/oe_fred_high_gpcrm_model1/bilayer_frames/rosetta-modeller-model1_frame_45')
outfile = open('/damsl/projects/molecules/data/Odorant_GPCR/gpcrm_model1_frame_45_scores_27Aug2013_odorator', 'w')
for score in scores_list:
    file_to_open = '/damsl/projects/molecules/data/Odorant_GPCR/receptor_models/olfr1393/oe_fred_high_gpcrm_model1/bilayer_frames/rosetta-modeller-model1_frame_45/' + score
    print 'now working on:', file_to_open
    for line in open(file_to_open,'r'):
        row_contribution = ''
        if line.startswith('Title'):
            print 'on title'
        else:
            col = line.split("\t")
            row_contribution = col[1] + " " + col[0] + '\n'
            outfile.write(row_contribution)
'''
