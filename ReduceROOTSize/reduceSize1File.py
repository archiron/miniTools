#! /usr/bin/env python
#-*-coding: utf-8 -*-

################################################################################
# reduceSize1File: a tool to reduce the size of the ROOT files, keeping only
# the used branches.
# for egamma validation comparison                              
#
# MUST be launched with the cmsenv cmd after a cmsrel cmd !!
#                                                                              
# Arnaud Chiron-Turlay LLR - arnaud.chiron@llr.in2p3.fr                        
#                                                                              
################################################################################

import os,sys, re

# lines below are only for func_Extract
from sys import argv
from os import listdir
from os.path import isfile, join

argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
argv.remove( '-b-' )

from ROOT import TFile

sys.path.append('../ChiLib')

def changeColor(color):
    # 30:noir ; 31:rouge; 32:vert; 33:orange; 34:bleu; 35:violet; 36:turquoise; 37:blanc
    # other references at https://misc.flogisoft.com/bash/tip_colors_and_formatting
    if (color == 'black'):
        return '[30m'
    elif (color == 'red'):
        return '[31m'
    elif (color == 'b_red'): # BOLD
        return '[1;31m'
    elif (color == 'green'):
        return '[32m'
    elif (color == 'orange'):
        return '[33m'
    elif (color == 'blue'):
        return '[34m'
    elif (color == ''):
        return '[35m'
    elif (color == 'purple'):
        return '[36m'
    elif (color == 'turquoise'):
        return '[37m'
    elif (color == 'lightyellow'):
        return '[93m'
    else:
        return '[30m'

def colorText(sometext, color):
    return '\033' + changeColor(color) + sometext + '\033[0m'

def changeDirectory(rootFile, path):
    """
    Change the current directory (ROOT.gDirectory) by the corresponding (rootFile,pathSplit)
    module from cmdLineUtils.py
    """
    rootFile.cd()
    theDir = ROOT.gDirectory.Get(path)
    if not theDir:
        print("Directory %s does not exist." % path)
    else:
        theDir.cd()
    return 0

def checkLevel(f_rel, f_out, path0, listkeys, nb, inPath, inp_file):
    #inPath = 'DQMData/Run 1/Info'
    #print('\npath : %s' % path0)
    if path0 != "":
        path0 += '/'
    
    for elem in listkeys:
        #print('%d == checkLevel : %s' % (nb, elem.GetTitle()))
        if (elem.GetClassName() == "TDirectoryFile"):
            path = path0 + elem.GetName()
            if (nb >= 3 and re.search(inPath, path)):
                #print('\npath : %s' % path)
                print('%s - path : %s' % (inp_file, path))
                f_out.mkdir(path)
            tmp = f_rel.Get(path).GetListOfKeys()
            checkLevel(f_rel, f_out, path, tmp, nb+1, inPath, inp_file)
        elif (elem.GetClassName() == "TTree"):
            #print('------ TTree')
            src = f_rel.Get(path0)
            cloned = src.CloneTree()
            #f_out.WriteTObject(cloned, elem.GetName())
            if (nb >= 3 and re.search(inPath, path0)):
                changeDirectory(f_out, path0[:-1])
                cloned.Write()
        elif (elem.GetClassName() != "TDirectory"):
            #print('copy %s object into %s path' % (elem.GetName(), path0[:-1]))
            #f_out.WriteTObject(elem.ReadObj(), elem.GetName())#:"DQMData/Run 1/EgammaV"
            if (nb >= 3 and re.search(inPath, path0)):
                changeDirectory(f_out, path0[:-1])
                elem.ReadObj().Write()

if len(sys.argv) > 1:
    print(sys.argv)
    print("step 1 - arg. 0 :", sys.argv[0]) # name of the script
    print("step 1 - arg. 1 :", sys.argv[1]) # name of the ROOT file
else:
    print("step 1 - rien")

print("func_ReduceSize")
input_file = sys.argv[1] # '/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO_' + '.root'
#input_file = input_file.replace('./', '/')
racine = input_file.split('.root')
output_file = racine[0] + 'b.root' # + racine[1]

#print('\n %s' % input_file)
#print('\n %s' % output_file)
print('\n {:s}'.format(colorText(input_file, 'b_red')))
print('{:s}\n'.format(colorText(output_file, 'b_red')))

paths = ['DQMData/Run 1/EgammaV', 'DQMData/Run 1/Info']

f_rel = ROOT.TFile(input_file, "UPDATE")
f_out = TFile(output_file, 'recreate')
t2 = f_rel.GetListOfKeys()

for elem in paths:
    checkLevel(f_rel, f_out, "", t2, 0, elem, input_file)

f_out.Close()
f_rel.Close()

tmp_file = './tmp' + '.root'
print('\n %s' % tmp_file)
print('move input_file to tmp_file')
os.rename(input_file, tmp_file) # mv input_file -> tmp_file
print('move output_file to input_file')
os.rename(output_file, input_file) # mv output_file -> input_file
print('delete tmp_file')
os.remove(tmp_file) # remove input_file

print("Fin !")

