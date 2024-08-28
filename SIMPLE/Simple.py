#! /usr/bin/env python
#-*-coding: utf-8 -*-

################################################################################
# Arnaud Chiron-Turlay LLR - arnaud.chiron@llr.in2p3.fr                         
################################################################################

import os,sys,shutil
import time
import importlib.machinery
import importlib.util

from graphicFunctions import Graphic
#from functions import *
#from config import * # WARNING, must be the local version and not the remote one !!!

from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kFatal # ROOT.kBreak # 
argv.remove( '-b-' )

def createDatasetFolder(folder):
    if not os.path.exists(folder): # create folder
        os.makedirs(folder) # create reference folder
        os.chdir(folder)
        # create gifs folders
        os.makedirs('gifs') # create gifs folder for pictures
        os.chdir('../')
    else: # folder already created
        os.chdir(folder)
        if not os.path.exists('gifs'): #
            # create gifs folders
            os.makedirs('gifs') # create gifs folder for pictures
        os.chdir('../')
    return

def shortHistoName(elem):
    histo_names = elem.split("/")
    histoShortNames = histo_names[1]
    histo_pos = histoShortNames
    histo_positions = histo_pos.split()
    short_histo_names = histoShortNames.split(" ")
    short_histo_name = short_histo_names[0].replace("h_", "")
    if "ele_" in short_histo_name:
        short_histo_name = short_histo_name.replace("ele_", "")
    if "scl_" in short_histo_name:
        short_histo_name = short_histo_name.replace("scl_", "")
    if "bcl_" in short_histo_name:
        short_histo_name = short_histo_name.replace("bcl_", "")
    return short_histo_name, short_histo_names, histo_positions

class Simple():
    def __init__(self):
        print('begin to run')
        gr = Graphic()
        gr.initRoot()

        Validation_reference = ''
 
        sys.path.append(os.getcwd()) # path where you work
        valEnv_d = os.getcwd()
        #tl = Tools()
        print('working in %s\n' % valEnv_d )
        web_repo = [valEnv_d, 'dev'] 
        print('Validation_reference : %s' % Validation_reference)
        print('web_repo : %s' % web_repo)

        listGeV = ['GeV_1']
        print(listGeV)

        # get time for begin
        start = time.time()           # let's see how long this takes

        for val in listGeV: # loop over GUI configurations
            #print('\n ***** %s ***** \n' % val)
            release = 'CMSSW_14_1_0_pre3'
            reference = 'CMSSW_14_1_0_pre3'
            print('long rel : %s' % release) # temp
            shortRelease = release[6:] # CMSSW_ removed
            shortReference = reference[6:] # CMSSW_ removed
            print('short rel : %s' % shortRelease) # temp
            releaseExtent = '2024'
            referenceExtent = ''
            print('rel extent : %s' % releaseExtent) # temp
            print('ref extent : %s' % referenceExtent) # temp
            choiceT = 'FullvsFull'
            print('choiceT : %s' % choiceT) # temp

            print('web repo : %s' % web_repo)
            relrefVT = ['RECO', 'RECO']
            print('relrefVT %s' % relrefVT)
            #Stop

            print('config relExtent %s' % releaseExtent)
            print('config refExtent %s' % referenceExtent)
            webFolder = web_repo[0] + '/GIFS/'

            if not os.path.exists(webFolder): # only create the first folder for saving gifs, i.e. release folder.
                self.exist_webFolder = False
            else:
                self.exist_webFolder = True

            if self.exist_webFolder: # True
                print("%s already created\n" % str(webFolder))
            else: # False
                os.makedirs(str(webFolder))

            datasets = ['ZEE_14']
            N = len(datasets)
            print('there is %d datasets : %s' % (N, datasets))

            print('')

            relFile = ['DQM_V0001_R000000001__RelValZEE_14__CMSSW_14_1_0_pre3-140X_mcRun3_2024_realistic_v8_STD_2024_noPU-v1__DQMIO.root']
            refFile = ['DQM_V0001_R000000001__RelValZEE_14__CMSSW_14_1_0_pre3-140X_mcRun3_2024_realistic_v8_STD_2024_noPU-v1__DQMIO.root']

            for i, elt in enumerate(datasets):
                dts = elt
                print('===== dataset : %s' % dts)
                print('len dataset : %d - len relFile : %d - len refFile : %d' % (len(datasets), len(relFile), len(refFile)))
                print('dataset : %s' % datasets)
                print('relFile : %s' % relFile)
                print('refFile : %s' % refFile)

                tp_1 = 'ElectronMcSignalValidator'
                tp_2 = tp_1
                print("tree path for target : %s" % tp_1)
                print("tree path for reference : %s" % tp_2)
                #Stop

                # create gifs pictures & web page
                CMP_TITLE = 'gedGsfElectrons ' + dts

                input_rel_file = valEnv_d + '/' + str(relFile[i])

                if not os.path.isfile(input_rel_file): # the rel root file does not exist
                    print('%s does not exist' % input_rel_file)
                    exit()
                else:
                    print(input_rel_file)

                f_rel = ROOT.TFile(input_rel_file)
                h1 = gr.getHisto(f_rel, tp_1)
                print('      h1 for dataset : %s' % dts)
                print(h1)

                input_ref_file = valEnv_d + '/' + str(refFile[i])

                if not os.path.isfile(input_ref_file): # the ref root file does not exist
                    print('%s does not exist' % input_ref_file)
                    exit()
                else:
                    print(input_ref_file)

                f_ref = ROOT.TFile(input_ref_file)
                h2 = gr.getHisto(f_ref, tp_2)
                print("input_rel_file = %s\n" % input_rel_file)
                print("input_ref_file = %s\n" % input_ref_file)
                print('      h2 for dataset : %s' % dts)
                #Stop
                
                # writing histos

                _, short_histo_names, histo_positions = shortHistoName('ElectronMcSignalValidator/h_ele_vertexEta              1 1 1 0')
                gif_name = "GIFS/" + short_histo_names[0] + ".gif"
                print('positions %s' % histo_positions)
                #Stop

                histo_1 = h1.Get(short_histo_names[0]) #
                histo_2 = h2.Get(short_histo_names[0]) #

                gr.PictureChoice(histo_1, histo_2, histo_positions[1], histo_positions[2], gif_name, 0) # 2

                os.chdir('../') # back to the final folder.

        # get time for end
        finish = time.time()
        print('total time to execute : %8.4f' % (finish-start)) # python2

        print('end of run')

