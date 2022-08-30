#! /usr/bin/env python
#-*-coding: utf-8 -*-

################################################################################
# GevSeqDev: a tool to generate Release Comparison                              
#
#
#                                                                              
# Arnaud Chiron-Turlay LLR - arnaud.chiron@llr.in2p3.fr                        
#                                                                              
################################################################################

import os,sys,subprocess
import re
import numpy as np
#import math

from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
#ROOT.gErrorIgnoreLevel = ROOT.kWarning # remove info like : Info in <TCanvas::Print>: gif file gifs/h_ele_vertexPhi.gif has been created
ROOT.gErrorIgnoreLevel = ROOT.kFatal
argv.remove( '-b-' )

from ROOT import * 

print('begin to run')
print('end of run')

