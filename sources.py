#! /usr/bin/env python
#-*-coding: utf-8 -*-

################################################################################
# sources.py : list of ROOT files to be used with zeeExtract tools
# for egamma validation comparison                              
# 
# MUST be launched with the cmsenv cmd after a cmsrel cmd !!
#                                                                              
# Arnaud Chiron-Turlay LLR - arnaud.chiron@llr.in2p3.fr                        
#                                                                              
################################################################################

# get the "new" root file datas
input_rel_file = 'DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_1_0_pre4-110X_mcRun3_2021_realistic_v8-v1__DQMIO.root'

# get the "reference" root file datas
input_ref_file = 'DQM_V0001_R000000001__RelValZEE_14__CMSSW_11_1_0_pre3-110X_mcRun3_2021_realistic_v8-v1__DQMIO.root'
#print('we use the %d file as reference' % ind_ref_file)
#print('we use : %s file as reference' % input_ref_file)

# histo name
histoName = 'h_recEleNum'

# path for the previous ROOT files
dataPath = 'DATA/'
