#! /usr/bin/env python
#-*-coding: utf-8 -*-

# MUST be launched with the cmsenv cmd after a cmsrel cmd !!

import os,sys,subprocess
import re

#import numpy as np

#import seaborn # only with cmsenv on cca.in2p3.fr

# lines below are only for func_Extract
from sys import argv

argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
argv.remove( '-b-' )

from ROOT import *
from sources import *

# these line for daltonians !
#seaborn.set_palette('colorblind')

def getHisto(file, tp):
    #t1 = file.Get("DQMData")
    #t2 = t1.Get("Run 1")
    #t3 = t2.Get("EgammaV")
    #t4 = t3.Get("Run summary")
    #t5 = t4.Get(tp)
    path = 'DQMData/Run 1/EgammaV/Run summary/' + tp
    t_path = file.Get(path)
    return t_path # t5

def RenderHisto(histo):

    if ("ELE_LOGY" in histo.GetOption() and histo.GetMaximum() > 0):
        cnv.SetLogy(1)
    histo_name_flag = 1 # use 0 to switch off
    if ( histo.InheritsFrom("TH2") ):
        gStyle.SetPalette(1)
        gStyle.SetOptStat(110+histo_name_flag)
    elif ( histo.InheritsFrom("TProfile") ):
        gStyle.SetOptStat(110+histo_name_flag)
    else: # TH1
        gStyle.SetOptStat(111110+histo_name_flag)

def createHistoPicture1(histo1, filename, linlog):
    cnv = TCanvas(str(0), "canvas")
    print('createPicture')
    color1 = ROOT.kRed #
    color0 = ROOT.kBlack
    color2 = ROOT.kBlue

    cnv.SetCanvasSize(960, 600)

    cnv.Clear()
    histo1.Draw()
    histo1.SetLineWidth(3)
    histo1.SetStats(1)
    #renderHisto(histo1)
    gPad.Update()
    statBox1 = histo1.GetListOfFunctions().FindObject("stats")
    histo1.SetLineColor(color0)
    histo1.SetMarkerColor(color1)
    statBox1.SetTextColor(color2)
    statBox1.SetFillStyle(0);
    statBox1.SetY1NDC(0.800)
    gPad.Update()

    if (linlog == "log"):
        cnv.SetLogy(1)
    cnv.Draw()
    cnv.Update()
    
    cnv.SaveAs(filename)

    return
    
def createHistoPicture2(histo1, histo2, scaled, err, filename, linlog):
    new_entries = histo1.GetEntries() # ttl # of bins (9000 in general)
    ref_entries = histo2.GetEntries()
    cnv = TCanvas(str(0), "canvas")
    color1 = ROOT.kRed #
    print(filename)

    histo2c = histo2.Clone()
    if ((scaled =="1") and (new_entries != 0) and (ref_entries != 0)):
        rescale_factor = new_entries / ref_entries
        histo2c.Scale(rescale_factor)
    if (histo2c.GetMaximum() > histo1.GetMaximum()):
        histo1.SetMaximum(histo2c.GetMaximum() * 1.1)
       
    cnv.SetCanvasSize(960, 900)
    cnv.Clear()
    cnv.SetFillColor(10)
    
    pad1 = ROOT.TPad(str(0), "pad1", 0, 0.25, 1.0, 1.0) # ,0,0,0
    pad1.SetBottomMargin(0.05)
    pad1.Draw()
    pad1.cd()
    
    if err == "1":
        newDrawOptions ="E1 P"
    else:
        newDrawOptions = "hist"
    
    histo1.SetStats(1)
    histo1.Draw(newDrawOptions) # 
    RenderHisto(histo1)
    if ("ELE_LOGY" in histo1.GetOption() and histo1.GetMaximum() > 0):
        if (re.search('etaEff_all', filename) or re.search('ptEff_all', filename)):
            print('accord')
            pad1.SetLogy(0)
        else:
            pad1.SetLogy(1)
    gPad.Update()
    statBox1 = histo1.GetListOfFunctions().FindObject("stats")
    statBox1.SetTextColor(color1)    
    gPad.Update()
    histo2c.Draw("sames hist") # ""  same
    histo2c.SetStats(1)
    RenderHisto(histo2c)
    if ("ELE_LOGY" in histo2c.GetOption() and histo2c.GetMaximum() > 0):
        if (re.search('etaEff_all', filename) or re.search('ptEff_all', filename)):
            print('accord')
            pad1.SetLogy(0)
        else:
            pad1.SetLogy(1)
    cnv.Update()
    statBox2 = histo2c.GetListOfFunctions().FindObject("stats")
    statBox2.SetTextColor(kBlue)
    y1 = statBox1.GetY1NDC()
    y2 = statBox1.GetY2NDC()
    statBox2.SetY1NDC(2*y1-y2)
    statBox2.SetY2NDC(y1)

    newDrawOptions = "sames "
    if err == "1":
        newDrawOptions += "E1 P"
    else:
        newDrawOptions += "hist"
    histo1.Draw(newDrawOptions)
    histo2c.Draw("sames hist")

    if (linlog == "log"):
        pad1.SetLogy(1)

    cnv.cd()
    pad2 = ROOT.TPad(str(0), "pad2", 0, 0.05, 1.00, 0.25) # ,0,0,0
    pad2.SetTopMargin(0.025)
    pad2.SetBottomMargin(0.2)
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    
    histo3 = histo1.Clone("histo3")
    histo3.SetLineColor(kBlack)
    histo3.SetMaximum(2.)
    histo3.SetMinimum(0.)
    histo3.SetStats(0)
    histo3.Sumw2() ########
    histo3.Divide(histo2)
    histo3.SetMarkerStyle(21)
    histo3.Draw("ep")
    
    histo1.SetMarkerColor(color1)
    histo1.SetLineWidth(3) 
    histo1.SetLineColor(color1)
    histo1.GetYaxis().SetTitleSize(25)
    histo1.GetYaxis().SetTitleFont(43)
    histo1.GetYaxis().SetTitleOffset(2.00)
    
    histo2c.SetLineColor(kBlue)
    histo2c.SetMarkerColor(kBlue)
    histo2c.SetLineWidth(3)
    
    histo3.SetTitle("")
    # Y axis ratio plot settings
    histo3.GetYaxis().SetTitle("ratio h1/h2 ")
    histo3.GetYaxis().SetNdivisions(505)
    histo3.GetYaxis().SetTitleSize(20)
    histo3.GetYaxis().SetTitleFont(43)
    histo3.GetYaxis().SetTitleOffset(1.55)
    histo3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
    histo3.GetYaxis().SetLabelSize(15)
    # X axis ratio plot settings
    histo3.GetXaxis().SetTitleSize(20)
    histo3.GetXaxis().SetTitleFont(43)
    histo3.GetXaxis().SetTitleOffset(4.)
    histo3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
    histo3.GetXaxis().SetLabelSize(15)

    cnv.Draw()
    cnv.Update()

    cnv.SaveAs(filename)
    
    return

if __name__=="__main__":

    tp = ['ElectronMcSignalValidator', 'ElectronMcSignalValidatorMiniAOD', 'ElectronMcFakeValidator', 'ElectronMcSignalValidatorPt1000']
    th = ['ElectronMcSignalHistos.txt', 'ElectronMcSignalHistosMiniAOD.txt', 'ElectronMcFakeHistos.txt', 'ElectronMcSignalHistosPt1000.txt']
    extent = ['_RECO', '_miniAOD', '_Fake', '_Pt1000']
    NB = len(extent)

    fileName_rel = dataPath + input_rel_file
    fileName_ref = dataPath + input_ref_file
    print('fileName rel : {:s}'.format(fileName_rel))
    print('fileName ref : {:s}'.format(fileName_ref))
    print('histoName : {:s}'.format(histoName))
    folder = histoName + '/'
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except OSError as e:
            if e.errno != errno.EEXIST: # the folder did not exist
                raise  # raises the error again
        print('Creation of %s release folder\n' % folder)
    else:
        print('Folder %s already created\n' % folder)

    fileRoot_rel = ROOT.TFile(fileName_rel)
    fileRoot_ref = ROOT.TFile(fileName_ref)
    for i in range(0,NB):
        f = open("HistosConfigFiles/" + th[i], "r")
        ll = f.readlines()
        f.close()
        datasetOK = False
        for elem in ll:
            if (re.search(histoName, elem)):
                print(elem)
                bb = ' '.join(elem.split()) # remove surnumerous white space
                aa = bb.split(' ')
                print(aa)
                scaled = aa[1]
                err = aa[2]
                datasetOK = True
                continue

        if (datasetOK):
            histo_rel = getHisto(fileRoot_rel, tp[i])
            histo_ref = getHisto(fileRoot_ref, tp[i])
            histo_rel = histo_rel.Get(histoName)
            histo_ref = histo_ref.Get(histoName)
            createHistoPicture1(histo_rel, folder + histoName + extent[i] + '_1.png', 'log')
            createHistoPicture2(histo_rel, histo_ref, scaled, err, folder + histoName + extent[i] + '_2.png', 'log')
    
    print("Fin !")

