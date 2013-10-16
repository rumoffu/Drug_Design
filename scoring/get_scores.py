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

def get_dock6_score_from_out():
	tautomer = 'F' #dock6 currently has no tautomer
	for out in os.listdir('.'):
		if 'dock6' in out and out.endswith('.out'):
        #for out in os.listdir('*dock6*out'):
			print 'working on: ' + receptor + ' ' + frame + ' ' + out
			if 'no' in out:
				response = '0.0'
				#continue##
			else:
				response = '1.0'
			infile = open(out, 'r')
			lines = infile.readlines()
			for line in lines:
				if 'Molecule:' in line:
					common_name = line[10:].strip()
					#if(',' in common_name): common_name = dashed(common_name)
					common_name, mysmile, mycompoundid = common_to_smile(common_name)
					#print 'name: %s smile: %s\n' % (common_name, mysmile)
        	                if 'Grid Score:' in line:
					grid_score = line[25:].strip()
				if 'Grid_vdw:' in line:
					grid_vdw = line[25:].strip()
				if 'Grid_es:' in line:
					grid_es = line[25:].strip()
				if 'Int_energy:' in line:
					int_energy = line[25:].strip()
					common_tautomer = common_name + ' ' + tautomer
					if common_tautomer not in seen:
						outline = str(mycompoundid)#mycompoundid
						outline += s + mysmile #smilestring
						outline += s + 'null' #ZINC_ID #assayname
						outline += s + 'null' #ACS_ID #CAS_ID #data
						outline += s + common_name #qualifier
						outline += s + response #result
						outline += s + 'null' #OdoratorID #unit
						outline += s + tautomer #'F'#tautomer #tautomers
						outline += s + 'sdf_fn'#sdf_fn 
						outline += s + 'smi_fn'#smi_fn
						outline += s + 'compound_dir' #compound_dir
						dinitialcompounds.write(outline + '\n')	
						seen.append(common_tautomer)

					global jobid
					jobid += 1
					jobline = str(jobid)#jobid
					jobline += s + str(framenum) #'1' #batch_id
					jobline += s + '2' #docker_id for dock6
					jobline += s + '1393' #receptor_id
					jobline += s + str(modelid) #model_id
					jobline += s + str(mycompoundid) #compound_id
					jobline += s + tautomer # 'F' #tautomers
					djobs.write(jobline + '\n')

					scoresline = str(jobid) #jobid
					scoresline += s + grid_score # gs 
					scoresline += s + grid_vdw # gvdw
					scoresline += s + grid_es # ges 
					scoresline += s + int_energy # inen 
					dock6scores.write(scoresline + '\n')				
	
#def get_dock6_score_from_out():
def get_fred_score_from_txt():
	for txt in os.listdir('.'):
		if '_score.txt' in txt: # and txt.endswith('.out'):
        #for out in os.listdir('*dock6*out'):
			if 'response' in txt:
				global response
				print 'working on: ' + receptor + '/' + txt #frame + ' ' + out
				if 'no' in txt:
					response = '0.0'
				else:
					response = '1.0'
				global tautomer
				if 'tautomers' in txt:
					tautomer = 'T'
				else:
					tautomer = 'F'
				infile = open(txt, 'r')
				lines = infile.readlines()
				for line in lines:
					if 'Title' in line: continue #ignore title line
					parsefred(line)

def parsefred(line):
	pieces = line.split('\t')
	assert(len(pieces) == 8)
	common_name = pieces[0]
	cg4 = pieces[1]
	steric = pieces[2]
	clash = pieces[3]
	pro_desolv = pieces[4]
	lig_desolv = pieces[5]
	lig_desolv_hb = pieces[6]
	cg4_hb = pieces[7].strip()
	#global seen
	common_name, mysmile, mycompoundid = common_to_smile(common_name)
	common_tautomer = common_name + ' ' + tautomer
	if common_tautomer not in seen:
	#if(',' in common_name): common_name = dashed(common_name)
                #outfile.write(grid_score + '\t' + molecule_name + '\n')
		#print grid_score, molecule_name # score
		#print '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (common_name, mysmile, mycompoundid, grid_score, grid_vdw, grid_es, int_energy)
		outline = str(mycompoundid)#mycompoundid
		outline += s + mysmile #smilestring
		outline += s + 'null' #ZINC_ID #assayname
		outline += s + 'null' #ACS_ID #CAS_ID #data
		outline += s + common_name #qualifier
		outline += s + response #result
		outline += s + 'null' #OdoratorID #unit
		outline += s + tautomer #tautomers
		outline += s + 'sdf_fn'#sdf_fn 
		outline += s + 'smi_fn'#smi_fn
		outline += s + 'compound_dir' #compound_dir
		initialcompounds.write(outline + '\n')	
		seen.append(common_tautomer)
		#print common_tautomer

	global jobid
	jobid += 1
	jobline = str(jobid)#jobid
	jobline += s + str(framenum) #batch_id
	jobline += s + '1' #1 for fred #docker_id
	jobline += s + '1393' #receptor_id
	jobline += s + str(modelid) #model_id
	jobline += s + str(mycompoundid) #compound_id
	jobline += s + tautomer #tautomers
	jobs.write(jobline + '\n')

	scoresline = str(jobid) #jobid
	scoresline += s + cg4 # gs 
	scoresline += s + steric # gvdw
	scoresline += s + clash # ges 
	scoresline += s + pro_desolv # inen 
	scoresline += s + lig_desolv
	scoresline += s + lig_desolv_hb
	scoresline += s + cg4_hb
	scoresline += s + bilayer # T or F for bilayer frames
	fredscores.write(scoresline.strip() + '\n')

def dashed(common_name):
	pieces = common_name.split()
	word = ''
	for p in pieces:
		word += p + '-'
	word = word[:-1]#cut off extra -
	return word
def common_to_smile(common_name):
	#print common_name
	if 'omega' in common_name:
		common_name, mysmile, mycompoundid = omega_to_common(common_name)
	else:
		smilefile = open(smile_fn,'r')
		for smilefile_line in smilefile:
			if common_name == smilefile_line.split('\t')[4]:
				mysmile = smilefile_line.split('\t')[1]
				mycompoundid = smilefile_line.split('\t')[0]
				#print 'mysmile: %s' % mysmile
				#print 'mycmpd_id: %s' % mycompoundid
	return common_name, mysmile, mycompoundid

def omega_to_common(common_name):
	omega_file = open('/damsl/projects/molecules/data/Odorant_GPCR/1393_test_no_response.smi', 'r')
	omega_file_lines = omega_file.readlines()
	k = -1
	#print common_name
	for i in range(1,8): #omega numbers
		k = k + 1
		txt = '' + str(i)
		if txt in common_name:
			mysmile = omega_file_lines[k].strip()
			#print mysmile
			smilefile = open(smile_fn, 'r')
			j = 0 #tracks line number
			for smilefile_line in smilefile:
				j = j + 1
				if mysmile in smilefile_line:
					common_name = smilefile_line.split('\t')[4]
					mycompoundid = j
					return common_name, mysmile, mycompoundid

#sets the modelid
def getModelid(receptor):
	global modelid
	modeloffset = 0
	if 'modeller' in receptor:
		modeloffset = 100
	if 'itasser' in receptor:
		modeloffset = 200
	modelid = (receptor.rsplit('_', 1)[1][5:]) #+ modeloffset
	if modelid != '': 
		modelid = int(modelid) + modeloffset
	else:
		if 'oe_fred_high' in receptor: modelid = 300
		elif 'dock6_finegrid_1u19' in receptor: modelid = 400
		else:	print "Error in modelid for %s" % receptor

#mysmile = ''                
mycompoundid = 0
#base_outfile = '/damsl/projects/molecules/data/Odorant_GPCR' #/Odorant_GPCR/db_kyle'
smile_fn = '/damsl/projects/molecules/data/Odorant_GPCR/initial_compounds_formatted_for_table_tab.separated2'
initialcompounds_fn = '/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/fredinitialcompounds.csv'
jobs_fn = '/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/fredlevel1_jobs.csv'
fredscores_fn = '/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/fredlevel1_fredscores.csv'

dinitialcompounds_fn = '/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/dock6initialcompounds.csv'
djobs_fn = '/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/dock6level1_jobs.csv'
dock6scores_fn = '/damsl/projects/molecules/data/Odorant_GPCR/db_kyle/dock6level1_dock6scores.csv'
global jobid #global jobid
jobid = 0
#jobid = 1334601 #fred went up to 1334601 jobs
#jobid = 3955 #dock6 last one was 3955

global seen
seen = []

global s
s = '\t' #separator character
global initialcompounds
global jobs
global fredscores
initialcompounds = open(initialcompounds_fn, 'a')
jobs = open(jobs_fn, 'a')
fredscores = open(fredscores_fn, 'a')

global dinitialcompounds
global djobs
global dock6scores
dinitialcompounds = open(dinitialcompounds_fn, 'a')
djobs = open(djobs_fn, 'a')
dock6scores = open(dock6scores_fn, 'a')
	
global bilayer
global modelid
global framenum
runfred = False
rundock6 = True
os.chdir('/damsl/projects/molecules/data/Odorant_GPCR/receptor_models/olfr1393')
for receptor in os.listdir('.'):
	if '_fred_high' in receptor and runfred:
		getModelid(receptor)
	#if 'oe_fred_high_gpcrm_model10' in receptor:
	#for receptor in os.listdir('dock6_grid_*'):
        	os.chdir(receptor)# + '/bilayer_frames')
        	for bilayerframes in os.listdir('.'):
			bilayer = 'F'
			#if not bilayerframes.endswith('_score.txt'): 
			if bilayerframes == 'bilayer_frames':
				os.chdir(bilayerframes)
				for frame in os.listdir('.'):
					if frame.endswith('.pdb'): continue
					if 'frame_' not in frame: continue
					framenum = str(frame.rsplit('_', 1)[1])
					if os.path.isdir(frame):
						os.chdir(frame)
						bilayer = 'T'
						get_fred_score_from_txt()
						os.chdir('..') #exit frame
				os.chdir('..') #exit score
		bilayer = 'F'
		framenum = '0' #not frame
		get_fred_score_from_txt()
        	os.chdir('..') # exit receptor #/..') #exit bilayer frames and receptor
	if 'dock6_grid_' in receptor and rundock6:
		getModelid(receptor)
		os.chdir(receptor + '/bilayer_frames')
		for frame in os.listdir('.'):
			if frame.endswith('.pdb'): continue
			if 'frame_' not in frame: continue
			framenum = str(frame.rsplit('_', 1)[1])
			if os.path.isdir(frame):
				os.chdir(frame)
				bilayer = 'T'
				get_dock6_score_from_out()
				os.chdir('..') #exit frame

		os.chdir('../..') #exit bilayer frames and receptor
	elif '_finegrid_' in receptor:
		continue
		#finish
		getModelid(receptor)
		frame = ''
		os.chdir(receptor)
		framenum = '0' #not frame
		get_dock6_score_from_out()
		os.chdir('..') #exit receptor

'''
	elif '_finegrid_' in receptor:
		continue
		#finish
		frame = ''
		os.chdir(receptor)
		get_dock6_score_from_out()
		os.chdir('..') #exit receptor
'''
initialcompounds.close()
jobs.close()
fredscores.close()
	
